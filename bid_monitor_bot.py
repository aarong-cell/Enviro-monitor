#!/usr/bin/env python3
"""
Public Bidding Monitor Bot - Cleveland, Ohio Demo
Monitors government procurement sites for stormwater, vac truck, and cleaning services
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
import re
from typing import List, Dict
import time

class BidMonitorBot:
    def __init__(self):
        self.keywords = [
            'stormwater', 'storm water', 'drainage', 'sewer',
            'vac truck', 'vacuum truck', 'vactor', 'hydro excavation',
            'cleaning', 'street cleaning', 'catch basin', 'storm drain',
            'jetting', 'pipe cleaning', 'sanitary sewer'
        ]
        
        self.opportunities = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def contains_keywords(self, text: str) -> bool:
        """Check if text contains any of our target keywords"""
        if not text:
            return False
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords)
    
    def scrape_cleveland_city(self):
        """Scrape City of Cleveland procurement opportunities"""
        print("🔍 Checking City of Cleveland...")
        
        try:
            url = "https://www.clevelandohio.gov/city-hall/departments/city-finance/purchasing-department"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                links = soup.find_all('a', href=True)
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link['href']
                    
                    if self.contains_keywords(link_text) or self.contains_keywords(href):
                        self.opportunities.append({
                            'source': 'City of Cleveland',
                            'title': link_text[:200],
                            'url': href if href.startswith('http') else f"https://www.clevelandohio.gov{href}",
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': 'Cleveland, OH',
                            'type': 'Municipal'
                        })
                
                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'City of Cleveland'])} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error scraping Cleveland: {str(e)}")
    
    def scrape_cuyahoga_county(self):
        """Scrape Cuyahoga County procurement opportunities"""
        print("🔍 Checking Cuyahoga County...")
        
        try:
            url = "https://cuyahogacounty.us/business/procurement"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                content = soup.get_text()
                links = soup.find_all('a', href=True)
                
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link['href']
                    
                    if self.contains_keywords(link_text):
                        self.opportunities.append({
                            'source': 'Cuyahoga County',
                            'title': link_text[:200],
                            'url': href if href.startswith('http') else f"https://cuyahogacounty.us{href}",
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': 'Cuyahoga County, OH',
                            'type': 'County'
                        })
                
                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'Cuyahoga County'])} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error scraping Cuyahoga County: {str(e)}")
    
    def scrape_ohio_state(self):
        """Scrape Ohio State procurement (DAS eProcurement)"""
        print("🔍 Checking Ohio State Procurement...")
        
        try:
            url = "https://procure.ohio.gov/Home"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                links = soup.find_all('a', href=True)
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link['href']
                    
                    if self.contains_keywords(link_text):
                        self.opportunities.append({
                            'source': 'State of Ohio',
                            'title': link_text[:200],
                            'url': href if href.startswith('http') else f"https://procure.ohio.gov{href}",
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': 'Ohio (Statewide)',
                            'type': 'State'
                        })
                
                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'State of Ohio'])} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error scraping Ohio State: {str(e)}")
    
    def add_sample_opportunities(self):
        """Add sample opportunities for demo purposes"""
        print("📋 Adding sample opportunities for demonstration...")
        
        samples = [
            {
                'source': 'City of Cleveland',
                'title': 'Storm Sewer Cleaning and CCTV Inspection Services - Annual Contract',
                'url': 'https://www.clevelandohio.gov/city-hall/departments/city-finance/purchasing-department',
                'posted_date': '2026-01-20',
                'deadline': '2026-02-15',
                'location': 'Cleveland, OH',
                'type': 'Municipal',
                'bid_number': 'CLV-2026-0045',
                'description': 'Annual contract for storm sewer cleaning, vac truck services, and CCTV inspection of municipal drainage systems'
            },
            {
                'source': 'Cuyahoga County',
                'title': 'Catch Basin Cleaning and Maintenance Services',
                'url': 'https://cuyahogacounty.us/business/procurement',
                'posted_date': '2026-01-18',
                'deadline': '2026-02-10',
                'location': 'Cuyahoga County, OH',
                'type': 'County',
                'bid_number': 'CC-PW-2026-012',
                'description': 'Countywide catch basin cleaning, storm drain maintenance, and vacuum truck services for stormwater infrastructure'
            },
            {
                'source': 'State of Ohio',
                'title': 'Stormwater Compliance and Drainage System Maintenance',
                'url': 'https://procure.ohio.gov/',
                'posted_date': '2026-01-15',
                'deadline': '2026-02-28',
                'location': 'Region 3 (Northeast Ohio)',
                'type': 'State',
                'bid_number': 'ODOT-SW-2026-089',
                'description': 'ODOT stormwater compliance services including drainage cleaning, vac truck operations, and regulatory reporting'
            },
            {
                'source': 'City of Cleveland',
                'title': 'Sanitary Sewer Jet Cleaning and Hydro Excavation Services',
                'url': 'https://www.clevelandohio.gov/city-hall/departments/city-finance/purchasing-department',
                'posted_date': '2026-01-22',
                'deadline': '2026-02-20',
                'location': 'Cleveland, OH',
                'type': 'Municipal',
                'bid_number': 'CLV-WTR-2026-0078',
                'description': 'Emergency and scheduled sewer cleaning using hydro-jetting and vacuum excavation equipment'
            },
            {
                'source': 'Cuyahoga County',
                'title': 'Street Sweeping and Storm Drain Cleaning - Zone 2',
                'url': 'https://cuyahogacounty.us/business/procurement',
                'posted_date': '2026-01-10',
                'deadline': '2026-02-05',
                'location': 'Cuyahoga County, OH',
                'type': 'County',
                'bid_number': 'CC-ENG-2026-003',
                'description': 'Combined street sweeping and storm drain cleaning services for eastern county municipalities'
            }
        ]
        
        self.opportunities.extend(samples)
        print(f"   ✓ Added {len(samples)} sample opportunities")
