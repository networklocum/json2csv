import requests
import json

import gen_outline
import json2csv


class Endpoint2CSV(object):
    expected_row_count = None
    results_index = "results"
    count_index = "count"
    outline_filename = 'temp.outline.json'

    def write_endpoint2csv(self, file_name, url):
        # requests can fail - usage of this method has to decide how to fail
        # (requests.exceptions.RequestException)
        first_response = requests.get(url)
        try:
            first_response = json.loads(first_response.content)
        except (ValueError, AttributeError) as e:
            raise requests.exceptions.RequestException(
                "Endpoint didn't return valid json. JSON parse error: {}".format(
                    str(e))
            )
        self.expected_row_count = first_response.get(self.count_index, False)
        if self.expected_row_count is False:
            raise requests.exceptions.RequestException(
                "Endpoint didn't return the number of rows in the first access "
                "of the paginated data."
            )

        one_page_of_results = first_response.get(self.results_index, False)
        if one_page_of_results is False:
            raise requests.exceptions.RequestException(
                "Endpoint didn't return '{}' on first page.".format(
                    self.results_index
                )
            )

        gen_outline.generate_outline(one_page_of_results, self.outline_filename)

        response = first_response

        next_page_url = response.get('next', False)
        if next_page_url is False:
            raise requests.exceptions.RequestException(
                "Endpoint didn't have a 'next' in the response json for "
                "pagination."
            )

        while next_page_url is not None:
            # This only happens on the first access of the endpoint.
            if response.get("next_page", False) == 2:
                json2csv.write_list_to_csv(
                    one_page_of_results,
                    file_name,
                    self.outline_filename,
                    open_mode="wb+"
                )
            else:
                json2csv.write_list_to_csv(
                    one_page_of_results,
                    file_name,
                    self.outline_filename,
                    open_mode="ab+"
                )

            next_page_url = response.get('next', False)
            if next_page_url is False:
                raise requests.exceptions.RequestException(
                    "Endpoint didn't have a 'next' in the response json for "
                    "pagination."
                )
            if next_page_url:
                response = requests.get(next_page_url)
                try:
                    response = json.loads(response.content)
                except (ValueError, AttributeError) as e:
                    raise requests.exceptions.RequestException(
                        "Endpoint didn't return valid json. "
                        "JSON parse error: {}".format(
                            str(e)
                        )
                    )
                one_page_of_results = response.get("results", False)
                if one_page_of_results is False:
                    raise requests.exceptions.RequestException(
                        "Endpoint didn't return 'results'."
                    )

    def check_report_validity(self):
        duplicate_rows = self.find_duplicate_rows()
        row_differences = self.find_length_differences()
        self.write_report_metadata(row_differences, duplicate_rows)

    # TODO
    def find_duplicate_rows(self):
        """
        :return: returns the duplicate rows (list of row #'s, the rows themselves?)
        """
        pass

    # TODO
    def find_row_differences(self):
        """
        :return: the difference between expected_row_count and the number of
        rows in the report
        """
        pass

    # TODO
    def write_report_metadata(self, row_differences, duplicate_rows):
        """
        Adds metadata to the csv file
        :param row_differences: the difference between the expected row count
        and the number of rows in the report
        :param duplicate_rows: the duplicate rows in the report
        :return:
        """
        pass

