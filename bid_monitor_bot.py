#!/usr/bin/env python3
"""
Enhanced Public Bidding Monitor Bot - All of Ohio
Monitors real government procurement sites across Ohio
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import re
from typing import List, Dict
import time

class BidMonitorBot:
    def __init__(self):
        self.keywords = [
            'stormwater', 'storm water', 'drainage', 'sewer',
            'vac truck', 'vacuum truck', 'vactor', 'hydro excavation',
            'cleaning', 'street cleaning', 'catch basin', 'storm drain',
            'jetting', 'pipe cleaning', 'sanitary sewer', 'sweeping',
            'npdes', 'ms4', 'erosion control'
        ]
        
        self.opportunities = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def contains_keywords(self, text: str) -> bool:
        """Check if text contains any of our target keywords"""
        if not text:
            return False
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords)
    
    def scrape_ohio_state_das(self):
        """Scrape Ohio DAS eProcurement - REAL DATA"""
        print("🔍 Checking Ohio DAS eProcurement System...")
        
        try:
            # Ohio's public procurement portal
            url = "https://procure.ohio.gov/ProcurePortal/search/solicitationSearch.do"
            
            # Search for open solicitations
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find solicitation links and tables
                tables = soup.find_all('table')
                links = soup.find_all('a', href=True)
                
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if self.contains_keywords(link_text) and len(link_text) > 10:
                        self.opportunities.append({
                            'source': 'Ohio DAS eProcurement',
                            'title': link_text[:200],
                            'url': href if href.startswith('http') else f"https://procure.ohio.gov{href}",
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': 'Ohio (Statewide)',
                            'type': 'State',
                            'bid_number': self._extract_bid_number(link_text)
                        })
                
                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'Ohio DAS eProcurement'])} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error scraping Ohio DAS: {str(e)}")
    
    def scrape_cleveland_city(self):
        """Scrape City of Cleveland - REAL DATA"""
        print("🔍 Checking City of Cleveland...")
        
        try:
            # Cleveland uses PlanetBids
            url = "https://www.clevelandohio.gov/city-hall/departments/city-finance/purchasing-department"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for bid documents and links
                links = soup.find_all('a', href=True)
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link['href']
                    
                    if self.contains_keywords(link_text) and len(link_text) > 15:
                        self.opportunities.append({
                            'source': 'City of Cleveland',
                            'title': link_text[:200],
                            'url': href if href.startswith('http') else f"https://www.clevelandohio.gov{href}",
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': 'Cleveland, OH',
                            'type': 'Municipal',
                            'bid_number': self._extract_bid_number(link_text)
                        })
                
                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'City of Cleveland'])} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error scraping Cleveland: {str(e)}")
    
    def scrape_columbus_city(self):
        """Scrape City of Columbus - REAL DATA"""
        print("🔍 Checking City of Columbus...")
        
        try:
            # Columbus procurement portal
            url = "https://www.columbus.gov/finance/purchasing/Bid-Opportunities/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                links = soup.find_all('a', href=True)
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link['href']
                    
                    if self.contains_keywords(link_text) and len(link_text) > 15:
                        self.opportunities.append({
                            'source': 'City of Columbus',
                            'title': link_text[:200],
                            'url': href if href.startswith('http') else f"https://www.columbus.gov{href}",
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': 'Columbus, OH',
                            'type': 'Municipal',
                            'bid_number': self._extract_bid_number(link_text)
                        })
                
                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'City of Columbus'])} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error scraping Columbus: {str(e)}")
    
    def scrape_cincinnati_city(self):
        """Scrape City of Cincinnati - REAL DATA"""
        print("🔍 Checking City of Cincinnati...")
        
        try:
            url = "https://www.cincinnati-oh.gov/procurement/bids/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                links = soup.find_all('a', href=True)
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link['href']
                    
                    if self.contains_keywords(link_text) and len(link_text) > 15:
                        self.opportunities.append({
                            'source': 'City of Cincinnati',
                            'title': link_text[:200],
                            'url': href if href.startswith('http') else f"https://www.cincinnati-oh.gov{href}",
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': 'Cincinnati, OH',
                            'type': 'Municipal',
                            'bid_number': self._extract_bid_number(link_text)
                        })
                
                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'City of Cincinnati'])} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error scraping Cincinnati: {str(e)}")
    
    def scrape_toledo_city(self):
        """Scrape City of Toledo - REAL DATA"""
        print("🔍 Checking City of Toledo...")
        
        try:
            url = "https://toledo.oh.gov/government/departments/law/purchasing"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                links = soup.find_all('a', href=True)
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link['href']
                    
                    if self.contains_keywords(link_text) and len(link_text) > 15:
                        self.opportunities.append({
                            'source': 'City of Toledo',
                            'title': link_text[:200],
                            'url': href if href.startswith('http') else f"https://toledo.oh.gov{href}",
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': 'Toledo, OH',
                            'type': 'Municipal',
                            'bid_number': self._extract_bid_number(link_text)
                        })
                
                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'City of Toledo'])} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error scraping Toledo: {str(e)}")
    
    def scrape_cuyahoga_county(self):
        """Scrape Cuyahoga County - REAL DATA"""
        print("🔍 Checking Cuyahoga County...")
        
        try:
            url = "https://cuyahogacounty.us/business/procurement"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                links = soup.find_all('a', href=True)
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link['href']
                    
                    if self.contains_keywords(link_text) and len(link_text) > 15:
                        self.opportunities.append({
                            'source': 'Cuyahoga County',
                            'title': link_text[:200],
                            'url': href if href.startswith('http') else f"https://cuyahogacounty.us{href}",
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': 'Cuyahoga County, OH',
                            'type': 'County',
                            'bid_number': self._extract_bid_number(link_text)
                        })
                
                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'Cuyahoga County'])} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error scraping Cuyahoga County: {str(e)}")
    
    def scrape_franklin_county(self):
        """Scrape Franklin County - REAL DATA"""
        print("🔍 Checking Franklin County...")
        
        try:
            url = "https://purchasing.franklincountyohio.gov/bids"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                links = soup.find_all('a', href=True)
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link['href']
                    
                    if self.contains_keywords(link_text) and len(link_text) > 15:
                        self.opportunities.append({
                            'source': 'Franklin County',
                            'title': link_text[:200],
                            'url': href if href.startswith('http') else f"https://purchasing.franklincountyohio.gov{href}",
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': 'Franklin County, OH',
                            'type': 'County',
                            'bid_number': self._extract_bid_number(link_text)
                        })
                
                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'Franklin County'])} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error scraping Franklin County: {str(e)}")
    
    def scrape_hamilton_county(self):
        """Scrape Hamilton County - REAL DATA"""
        print("🔍 Checking Hamilton County...")
        
        try:
            url = "https://www.hamiltoncountyohio.gov/business/purchasing"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                links = soup.find_all('a', href=True)
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link['href']
                    
                    if self.contains_keywords(link_text) and len(link_text) > 15:
                        self.opportunities.append({
                            'source': 'Hamilton County',
                            'title': link_text[:200],
                            'url': href if href.startswith('http') else f"https://www.hamiltoncountyohio.gov{href}",
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': 'Hamilton County, OH',
                            'type': 'County',
                            'bid_number': self._extract_bid_number(link_text)
                        })
                
                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'Hamilton County'])} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error scraping Hamilton County: {str(e)}")
    
    def scrape_bidnet_direct(self):
        """Scrape BidNet Direct - Major Ohio procurement platform"""
        print("🔍 Checking BidNet Direct (Ohio agencies)...")
        
        try:
            # BidNet hosts many Ohio municipalities
            url = "https://www.bidnetdirect.com/ohio"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for bid listings
                bid_elements = soup.find_all(['div', 'tr'], class_=re.compile(r'bid|solicitation', re.I))
                
                for element in bid_elements[:20]:  # Limit to prevent overwhelming
                    text = element.get_text(strip=True)
                    if self.contains_keywords(text) and len(text) > 20:
                        links = element.find_all('a', href=True)
                        if links:
                            link = links[0]
                            href = link['href']
                            self.opportunities.append({
                                'source': 'BidNet Direct (Ohio)',
                                'title': text[:200],
                                'url': href if href.startswith('http') else f"https://www.bidnetdirect.com{href}",
                                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                                'location': 'Various Ohio Locations',
                                'type': 'Municipal',
                                'bid_number': self._extract_bid_number(text)
                            })
                
                print(f"   ✓ Found {len([o for o in self.opportunities if 'BidNet' in o['source']])} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error scraping BidNet: {str(e)}")
    
    def _extract_bid_number(self, text: str) -> str:
        """Extract bid/RFP number from text"""
        patterns = [
            r'#[\dA-Z-]+',
            r'RFP[\s-]?[\dA-Z-]+',
            r'BID[\s-]?[\dA-Z-]+',
            r'IFB[\s-]?[\dA-Z-]+',
            r'\d{4,}[-/]\d+',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return ''
    
    def deduplicate_opportunities(self):
        """Remove duplicate opportunities based on title similarity"""
        seen = set()
        unique_opps = []
        
        for opp in self.opportunities:
            # Create a signature from title (first 100 chars, lowercase, no spaces)
            signature = opp['title'][:100].lower().replace(' ', '')
            
            if signature not in seen:
                seen.add(signature)
                unique_opps.append(opp)
        
        removed = len(self.opportunities) - len(unique_opps)
        if removed > 0:
            print(f"🔄 Removed {removed} duplicate opportunities")
        
        self.opportunities = unique_opps
    
    def run_all_scrapers(self):
        """Run all scrapers for Ohio"""
        print("\n" + "="*70)
        print("🤖 OHIO STATEWIDE BID MONITOR")
        print("="*70)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # State level
        self.scrape_ohio_state_das()
        time.sleep(2)
        
        # Major cities
        self.scrape_cleveland_city()
        time.sleep(2)
        self.scrape_columbus_city()
        time.sleep(2)
        self.scrape_cincinnati_city()
        time.sleep(2)
        self.scrape_toledo_city()
        time.sleep(2)
        
        # Major counties
        self.scrape_cuyahoga_county()
        time.sleep(2)
        self.scrape_franklin_county()
        time.sleep(2)
        self.scrape_hamilton_county()
        time.sleep(2)
        
        # Aggregator platforms
        self.scrape_bidnet_direct()
        time.sleep(2)
        
        # Remove duplicates
        self.deduplicate_opportunities()
        
        print()
        print("="*70)
        print(f"✅ Scan Complete - Found {len(self.opportunities)} unique opportunities")
        print("="*70)
        
        return self.opportunities

if __name__ == "__main__":
    bot = BidMonitorBot()
    bot.run_all_scrapers()
    print(f"\n📊 Results: {len(bot.opportunities)} opportunities found")
