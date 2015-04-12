from bs4 import BeautifulSoup
import re

def regex_page_data_int(pattern, html):
    """Extract an integer value from the page based on a pattern."""
    result = regex_page_data(pattern, html)
    if result is not None:
        if ',' in result:
            result = result.replace(',', '')
        result = int(result)
    return result


def regex_page_data_float(pattern, html):
    """Extract a floating point value from the page based on a pattern."""
    result = regex_page_data(pattern, html)
    if result is not None:
        if ',' in result:
            result = result.replace(',', '')
        result = float(result)
    return result


def regex_page_data_table(pattern, html):
    """Extract data from a table on the page based on an id and value."""
    soup = BeautifulSoup(html)
    attributes = pattern.split('=')
    table_data = []
    table = soup.find("table", attrs={attributes[0]:attributes[1]})

    if table is not None:
        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        # Format the headings
        for idx, item in enumerate(headings):
            headings[idx] = re.sub('[!@#$]', '', item.lower().replace(' ', '_'))

        # Iterate the table and parse the data
        for row in table.findAll("tr")[1:]:
            cells = row.findAll("td")
            row_data = {}
            for i in range(0, len(cells) -1):
                row_data[headings[i]] = cells[i].get_text()

                # Look for links which do not match the text and fix them
                cell_link = cells[i].find('a')
                if cell_link is not None:
                    last_element = cell_link.get('href').split('/')[-1]
                    if last_element.replace('_', ' ') != row_data[headings[i]]:
                        row_data[headings[i]] = last_element.replace('_', ' ')

            table_data.append(row_data)
        return table_data
    else:
        return None


def regex_page_data(pattern, html):
    """Get a value from page data based on a regex pattern. """
    result = re.search(pattern, html)
    if result is not None:
        return result.group(1)
    else:
        return None