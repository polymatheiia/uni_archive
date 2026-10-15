#!/usr/bin/env python3
"""
Complete Flu Data Extraction Script for Poland 2007-2023
Extracts weekly flu data from PZH PDFs and formats it to match the Excel structure
"""

import requests
import re
import pandas as pd
from io import BytesIO
from PyPDF2 import PdfReader
import time
from datetime import datetime
from collections import defaultdict

def generate_pdf_urls(years):
    """Generate all possible PDF URLs for given years"""
    urls = []
    for year in years:
        yy = str(year)[-2:]
        for month in range(1, 13):
            for letter in ['A', 'B', 'C', 'D']:
                url = f"https://wwwold.pzh.gov.pl/oldpage/epimeld/grypa/{year}/G_{yy}_{month:02d}{letter}.pdf"
                urls.append({
                    'year': year,
                    'month': month,
                    'letter': letter,
                    'url': url
                })
    return urls

def download_pdf(url, timeout=10):
    """Download PDF from URL"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return BytesIO(response.content)
        return None
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def parse_flu_data(text, year, month, letter):
    """Extract structured flu data from PDF text"""
    data = {
        'year': year,
        'month': month,
        'letter': letter,
        'period': None,
        'week_number': None,
        'national_data': {},
        'voivodeship_data': []
    }
    
    # Extract period
    period_match = re.search(r'Okres:\s*(\d+)\s*[–-]\s*(\d+)\s+(\w+)', text)
    if period_match:
        data['period'] = f"{period_match.group(1)}-{period_match.group(2)} {period_match.group(3)}"
    
    # Extract week number
    week_match = re.search(r'tydzień\s+(\d+)', text)
    if week_match:
        data['week_number'] = int(week_match.group(1))
    
    # Voivodeships to extract
    voivodeships = [
        'POLSKA', 'Dolnośląskie', 'Kujawsko-Pomorskie', 'Lubelskie', 'Lubuskie',
        'Łódzkie', 'Małopolskie', 'Mazowieckie', 'Opolskie', 'Podkarpackie',
        'Podlaskie', 'Pomorskie', 'Śląskie', 'Świętokrzyskie',
        'Warmińsko-Mazurskie', 'Wielkopolskie', 'Zachodniopomorskie'
    ]
    
    # Extract data for each voivodeship
    for voiv in voivodeships:
        # Pattern: Name total incidence change age0-4_n age0-4_inc age5-14_n age5-14_inc age15-64_n age15-64_inc age65+_n age65+_inc
        pattern = rf'{voiv}\s+(\d+)\s+([\d,\.]+)\s+([–\-]?[\d,\.]+)\s+(\d+)\s+([\d,\.]+)\s+(\d+)\s+([\d,\.]+)\s+(\d+)\s+([\d,\.]+)\s+(\d+)\s+([\d,\.]+)'
        match = re.search(pattern, text)
        
        if match:
            record = {
                'voivodeship': voiv,
                'total_cases': int(match.group(1)),
                'incidence_per_100k': float(match.group(2).replace(',', '.')),
                'age_0_4_cases': int(match.group(4)),
                'age_0_4_incidence': float(match.group(5).replace(',', '.')),
                'age_5_14_cases': int(match.group(6)),
                'age_5_14_incidence': float(match.group(7).replace(',', '.')),
                'age_15_64_cases': int(match.group(8)),
                'age_15_64_incidence': float(match.group(9).replace(',', '.')),
                'age_65plus_cases': int(match.group(10)),
                'age_65plus_incidence': float(match.group(11).replace(',', '.'))
            }
            
            if voiv == 'POLSKA':
                data['national_data'] = record
            else:
                data['voivodeship_data'].append(record)
    
    return data

def process_all_pdfs(years):
    """Download and process all PDFs for given years"""
    urls = generate_pdf_urls(years)
    all_data = []
    
    print(f"Processing {len(urls)} potential PDFs...")
    
    for i, url_info in enumerate(urls):
        if (i + 1) % 10 == 0:
            print(f"Progress: {i+1}/{len(urls)}")
        
        pdf_file = download_pdf(url_info['url'])
        if pdf_file:
            text = extract_text_from_pdf(pdf_file)
            if text:
                data = parse_flu_data(text, url_info['year'], url_info['month'], url_info['letter'])
                if data['national_data']:  # Only add if we extracted data
                    all_data.append(data)
        
        time.sleep(0.5)  # Be polite to the server
    
    print(f"Successfully extracted data from {len(all_data)} PDFs")
    return all_data

def create_excel_output(all_data, output_file):
    """Create Excel file with three tables matching the format"""
    
    # Tabela 1: National weekly data
    tabela1 = []
    for record in all_data:
        if record['national_data']:
            tabela1.append({
                'Choroba': 'Grypa',
                'Rok': record['year'],
                'Numer tygodnia': record['week_number'] or 0,
                'Liczba przypadków na 100 tys.': record['national_data']['incidence_per_100k']
            })
    
    # Tabela 2: By age groups
    tabela2 = []
    for record in all_data:
        if record['national_data']:
            nat = record['national_data']
            for age_group, incidence in [
                ('0-4', nat['age_0_4_incidence']),
                ('5-14', nat['age_5_14_incidence']),
                ('15-64', nat['age_15_64_incidence']),
                ('65+', nat['age_65plus_incidence'])
            ]:
                tabela2.append({
                    'Choroba': 'Grypa',
                    'Rok': record['year'],
                    'Numer tygodnia': record['week_number'] or 0,
                    'Kategoria wiekowa': age_group,
                    'Liczba przypadków na 100 tys.': incidence
                })
    
    # Tabela 3: By voivodeship
    tabela3 = []
    for record in all_data:
        for voiv_data in record['voivodeship_data']:
            tabela3.append({
                'Choroba': 'Grypa',
                'Rok': record['year'],
                'Numer tygodnia': record['week_number'] or 0,
                'Województwo': voiv_data['voivodeship'],
                'Liczba przypadków na 100 tys.': voiv_data['incidence_per_100k']
            })
    
    # Create Excel file
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        pd.DataFrame(tabela1).to_excel(writer, sheet_name='Tabela 1', index=False)
        pd.DataFrame(tabela2).to_excel(writer, sheet_name='Tabela 2', index=False)
        pd.DataFrame(tabela3).to_excel(writer, sheet_name='Tabela 3', index=False)
    
    print(f"✓ Excel file created: {output_file}")
    print(f"  - Tabela 1 (National): {len(tabela1)} rows")
    print(f"  - Tabela 2 (By Age): {len(tabela2)} rows")
    print(f"  - Tabela 3 (By Voivodeship): {len(tabela3)} rows")

if __name__ == "__main__":
    print("Flu Data Extraction Script for Poland 2007-2023")
    print("=" * 60)
    
    # Extract data for 2007 to 2023
    all_data = process_all_pdfs([2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
    
    # Create output file
    output_file = "grypa_polska_2007_2023_historical.xlsx"
    create_excel_output(all_data, output_file)
    
    print(f"\n✓ Complete! Output saved to: {output_file}")
