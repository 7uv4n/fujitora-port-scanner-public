from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import json
from helpers.helper import expand_ip_range
from helpers.helper import expand_ranges
from helpers.scanner import scan_multiple_ips
import pdfkit
from flask import render_template, request, Response

from flask import render_template, request, jsonify, send_file
from flask import current_app as app
import sqlite3

# Initialize SQLite Database
conn = sqlite3.connect('scan_results.db')
cursor = conn.cursor()

# Create a table to store scan results if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY,
    name TEXT,
    ip_address TEXT,
    portnumbers TEXT,
    scan_results TEXT,
    start_time TEXT,
    end_time TEXT,
    elapsed_time FLOAT,
    scan_summary_filename_json TEXT,
    scan_summary_filename_html TEXT,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

''')
conn.commit()

app = Flask(__name__)

navbar = """
    <a class="navbar-brand" href="/">Fujitora Port Scanner</a>
    <a class="navbar-brand" href="/previous">Previous Tests</a>
"""
#
#
#
#
#
# This route will be used to display the home page
@app.route('/')
def index():
    return render_template('index.html' , navbar = navbar)

@app.route('/result', methods=['POST'])
def result():
    conn = sqlite3.connect('scan_results.db')
    cursor = conn.cursor()

    name = request.form['Name']
    ip_address = request.form['ip_address']
    portnumbers = request.form['portnumbers']
    ip_addresses = expand_ip_range(ip_address)
    portnumbers_ = expand_ranges(portnumbers)

    scan_results = scan_multiple_ips(ip_addresses, portnumbers_, name)

    if name in scan_results:
        result = scan_results[name][0]
        ip = result['ip']
        open_ports = result['open_ports']
        closed_ports = result['closed_ports']
        filtered_ports = result['filtered_ports']
        start_time = result['start_time']
        end_time = result['end_time']
        elapsed_time = result['elapsed_time']

        # Convert start_time and end_time to string format
        start_time_str = str(start_time)
        end_time_str = str(end_time)
        elapsed_time_float = float(elapsed_time)

        # Convert scan_results to JSON
        scan_results_json = json.dumps(scan_results)

        # Generate file name
        file_name = f"{name}_{end_time_str.replace(':', '-')}_scan_summary"

        # Define file paths
        file_path_json = f"{file_name}.json"
        file_path_html = f"{file_name}.html"

        # Insert data into SQLite
        cursor.execute('''
            INSERT INTO scans 
            (name, ip_address, portnumbers, scan_results, start_time, end_time, elapsed_time, scan_summary_filename_json, scan_summary_filename_html)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, ip_address, portnumbers, scan_results_json, start_time_str, end_time_str, elapsed_time_float, file_path_json, file_path_html))

        conn.commit()

        # Output the result to a JSON file
        with open(f"blob_storage/{file_name}.json", "w") as json_file:
            json.dump(scan_results, json_file, indent=4)

        RENDER = render_template('result.html', json_data=scan_results, navbar=navbar, name=name)

        with open(f"templates/{file_name}.html", 'w') as file:
            file.write(RENDER)

        return RENDER
    else:
        return "Scan results not found for the specified name."


# This route will be used to display the previous scan results
@app.route('/previous')
def prev_results():
    conn = sqlite3.connect('scan_results.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scans order by id desc')
    previous_scans = cursor.fetchall()
    return render_template('prev_tests.html', previous_scans=previous_scans, navbar = navbar)

# This route will be used to display the scan summary
@app.teardown_appcontext
def close_connection(exception=None):
    conn = sqlite3.connect('scan_results.db')
    if conn is not None:
        conn.close()

# This route will be used to download the scan summary as a JSON payload
@app.route('/download/<filename>')
def download_file(filename):
    file_path = f'blob_storage/{filename}'
    return send_file(file_path, as_attachment=True)

# This route will be used to delete a scan entry
@app.route('/delete/<int:id>')
def delete_entry(id):
    conn = sqlite3.connect('scan_results.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM scans WHERE id = ?', (id,))
    conn.commit()
    return redirect(url_for('prev_results'))


@app.route('/prev_dashboard/<string:webs>')
def prev_dashboard(webs):
    print(webs)
    return render_template(webs)

if __name__ == '__main__':
    app.run(debug=True)