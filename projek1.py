from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt
import os
import random

app = Flask(__name__, static_url_path='/static')

plt.switch_backend('agg')

@app.route('/', methods=['GET', 'POST'])
def monitor():
    url = ""
    response_data = {}
    img_paths = {}
    visitor_data = None
    
    if request.method == 'POST':
        url = request.form.get('url')
        date = request.form.get('date')
        month = request.form.get('month')
        year = request.form.get('year')

        if date is not None and month is not None and year is not None:
            date = int(date)
            month = int(month)
            year = int(year)
        else:
            date = 1
            month = 1
            year = 2023

        if url:
            try:
                response = requests.get(url)
                response_data = {
                    'URL': url,
                    'Status Code': response.status_code,
                    'Response Time (s)': response.elapsed.total_seconds()
                }
                visitor_data = scrape_visitor_data(date, month, year)
                img_paths['gender_histogram'] = create_gender_histogram(visitor_data['gender'])
                img_paths['line_chart'] = create_line_chart(visitor_data['average_age'])
                img_paths['pie_chart'] = create_pie_chart(visitor_data['visitor_count'])
                img_paths['bar_chart'] = create_bar_chart(visitor_data['visit_duration'])
            except Exception as e:
                response_data = {
                    'URL': url,
                    'Status Code': 'Error',
                    'Response Time (s)': 'N/A'
                }
    return render_template('index.html', url=url, response_data=response_data, img_paths=img_paths)

def scrape_visitor_data(date, month, year):
    random.seed(year * 10000 + month * 100 + date)
    visitor_data = {
        'visitor_count': [random.randint(10, 50) for _ in range(5)],
        'average_age': [random.randint(20, 60) for _ in range(5)],
        'visit_duration': [random.randint(1, 10) for _ in range(30)],
        'gender': [random.choice(['laki laki', 'perempuan']) for _ in range(5)]
    }
    return visitor_data

def create_gender_histogram(gender_data):
    
    male_count = gender_data.count('laki laki')
    female_count = gender_data.count('perempuan')
    total_count = len(gender_data)

    male_percentage = (male_count / total_count) * 100
    female_percentage = (female_count / total_count) * 100

    labels = ['laki laki', 'perempuan']
    percentages = [male_percentage, female_percentage]

    plt.bar(labels, percentages, color=['blue', 'pink'])
    plt.xlabel('Jenis Kelamin')
    plt.ylabel('Persentase')
    plt.title('Gender Distribusi')

    img_path = os.path.join('static', 'gender_histogram.png')
    plt.savefig(img_path, format='png')
    plt.clf()

    return img_path

def create_line_chart(data):
    
    x = list(range(len(data)))
    y = data

    plt.plot(x, y)
    plt.xlabel('Hari')
    plt.ylabel('Rata-rata Umur')
    plt.title('Grafik Rata-rata Umur Pengunjung')

    img_path = os.path.join('static', 'line_chart.png')
    plt.savefig(img_path, format='png')
    plt.clf()

    return img_path

def create_pie_chart(data):
    
    labels = ['Hari 1', 'Hari 2', 'Hari 3', 'Hari 4', 'Hari 5']  
    sizes = data 

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Diagram Pie Chart Jumlah Pengunjung')

    img_path = os.path.join('static', 'pie_chart.png')
    plt.savefig(img_path, format='png')
    plt.clf()

    return img_path

def create_bar_chart(data):
    
    categories = list(range(1, len(data) + 1))
    values = data

    plt.bar(categories, values)
    plt.xlabel('Hari')
    plt.ylabel('Durasi Kunjungan (menit)')
    plt.title('Diagram Batang Durasi Kunjungan Pengunjung')

    img_path = os.path.join('static', 'bar_chart.png')
    plt.savefig(img_path, format='png')
    plt.clf()

    return img_path

if __name__ == '__main__':
    app.run(debug=True)
