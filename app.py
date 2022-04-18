from flask import Flask, request, redirect, url_for
import csv

app = Flask(__name__)

stylesheet = """
        <style>
            table, th, td {
              border: 1px solid black;
              border-collapse: collapse;
            }
            th, td {
              padding: 5px;
            }
        </style>
        """

def get_index_for_category(cat):
    if cat == 'name':
        index = 1
    elif cat == 'pin':
        index = 5
    elif cat == 'score':
        index = 10
    return index

@app.route('/jee2009/name/<value>')
def get_from_name(value):
    return get_records_for_category(value, 'name')

@app.route('/jee2009/pin/<value>')
def get_from_pin(value):
    return get_records_for_category(value, 'pin')

@app.route('/jee2009/score/<value>')
def get_from_score(value):
    return get_records_for_category(value, 'score', exact_match=True)

def get_records_for_category(value, category, exact_match=False):
    if not value:
        return 'Enter valid {}'.format(category)
    line_count = 0
    results = []
    header = None
    with open('/home/karanbajaj23/jee2009/jee2009.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                header = row
                line_count += 1
                continue
            else:
                line_count += 1
                row_value = row[get_index_for_category(category)]
                if (exact_match and value.lower() == row_value.lower()) or (value.lower() in row_value.lower()):
                    results.append(row)
    if results:
        results = sorted(results, key=lambda x: int(x[10]), reverse=True)
        results = [header] + results
        html = stylesheet
        html += '<h2>Total records found: {}</h2><br>'.format(len(results))
        html += '<table>'
        for res in results:
            html += '<tr>'
            for k in res:
                html += '<td>{}</td>'.format(k)
            html += '</tr>'
        html += '</table>'
        return html
    return 'Not found. Total parsed records: {}'.format(line_count-1)

@app.route('/jee2009/rank/<rank>')
def get_from_rank(rank):
    if not rank:
        return 'Enter valid rank'
    rank = int(rank)
    line_count = 0
    all_candidates = []
    with open('/home/karanbajaj23/jee2009/jee2009.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            else:
                line_count += 1
                all_candidates.append(row)
    all_candidates = sorted(all_candidates, key=lambda x: int(x[10]), reverse=True)
    res = None
    if rank <= line_count-1:
        res = all_candidates[rank-1]
    if res:
        html = stylesheet
        html += '<table>'
        html += '<tr>'
        for k in res:
            html += '<td>{}</td>'.format(k)
        html += '</tr>'
        html += '</table>'
        return html
    return 'Not found. Total parsed records: {}'.format(line_count-1)

@app.route('/')
def home():
    return redirect(url_for('home_jee2009'))

@app.route('/jee2009')
def home_jee2009():
    html = '<html>'
    name_url = url_for('get_from_name', value='nitin jain')
    pin_url = url_for('get_from_pin', value='121001')
    score_url = url_for('get_from_score', value='100')
    html += '<h3>Reference:</h3>'
    html += '<p>Using name: <a href="' + name_url + '">' + name_url + '</a></p>'
    html += '<p>Using PIN code: <a href="' + pin_url + '">' + pin_url + '</a></p>'
    html += '<p>Using total score: <a href="' + score_url + '">' + score_url + '</a></p>'
    html += '</html>'
    return html

