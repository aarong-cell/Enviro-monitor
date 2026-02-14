#!/usr/bin/env python3
"""
Ultimate Ohio Public Bidding Monitor Bot
Comprehensive statewide coverage with expanded water infrastructure keywords
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
        # EXPANDED KEYWORDS - Water Infrastructure Focus
        self.keywords = [
            # Stormwater & Drainage
            'stormwater', 'storm water', 'storm sewer', 'drainage', 'storm drain',
            'catch basin', 'catch basins', 'inlet', 'outfall', 'culvert',
            'retention pond', 'detention basin', 'bioswale', 'swale',
            'npdes', 'ms4', 'erosion control', 'sediment control',
            
            # Sewer Systems
            'sewer', 'sanitary sewer', 'wastewater', 'waste water',
            'sewer line', 'sewer main', 'sewer lateral', 'manhole',
            'lift station', 'pump station', 'force main',
            
            # Vac Truck & Equipment
            'vac truck', 'vacuum truck', 'vactor', 'combination truck',
            'sewer cleaner', 'jet vac', 'suction excavator',
            'hydro excavation', 'vacuum excavation', 'potholing',
            
            # Cleaning & Maintenance
            'cleaning', 'clean', 'flushing', 'jetting', 'hydro jetting',
            'jet cleaning', 'pipe cleaning', 'line cleaning',
            'street sweeping', 'sweeping', 'power sweeping',
            'debris removal', 'sediment removal',
            
            # Inspection & CCTV
            'cctv', 'video inspection', 'camera inspection', 'televising',
            'pipeline inspection', 'sewer inspection', 'lateral inspection',
            'smoke testing', 'dye testing', 'manhole inspection',
            
            # Rehabilitation & Repair
            'pipe lining', 'cipp', 'trenchless', 'slip lining',
            'pipe bursting', 'point repair', 'spot repair',
            'manhole rehabilitation', 'manhole repair',
            
            # Water Infrastructure
            'water main', 'water line', 'water distribution',
            'valve exercising', 'fire hydrant', 'water meter',
            'backflow', 'cross connection',
            
            # Construction & Engineering
            'utility', 'infrastructure', 'public works',
            'basin cleaning', 'ditch cleaning', 'channel cleaning',
            'grading', 'excavation', 'sitework'
        ]
        
        self.opportunities = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        
        self.timeout = 10
    
    def contains_keywords(self, text: str) -> bool:
        """Check if text contains any of our target keywords"""
        if not text:
            return False
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords)
    
    def safe_scrape(self, url: str, source_name: str, location: str, bid_type: str):
        """Generic scraper with error handling"""
        print(f"🔍 Checking {source_name}...")
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find all links
                links = soup.find_all('a', href=True)
                count = 0
                
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    # Check if link text or surrounding context matches keywords
                    parent_text = link.parent.get_text(strip=True) if link.parent else ''
                    combined_text = f"{link_text} {parent_text}"
                    
                    if self.contains_keywords(combined_text) and len(link_text) > 15:
                        # Build full URL
                        if href.startswith('http'):
                            full_url = href
                        elif href.startswith('/'):
                            base_url = '/'.join(url.split('/')[:3])
                            full_url = f"{base_url}{href}"
                        else:
                            full_url = url
                        
                        self.opportunities.append({
                            'source': source_name,
                            'title': link_text[:250],
                            'url': full_url,
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': location,
                            'type': bid_type,
                            'bid_number': self._extract_bid_number(link_text),
                            'description': parent_text[:300] if len(parent_text) > len(link_text) else ''
                        })
                        count += 1
                
                print(f"   ✓ Found {count} opportunities")
                return True
            else:
                print(f"   ⚠ HTTP {response.status_code}")
                return False
            
        except Exception as e:
            print(f"   ⚠ Error: {str(e)[:100]}")
            return False
    
    # STATE LEVEL
    def scrape_ohio_state_das(self):
        """Ohio DAS eProcurement System"""
        self.safe_scrape(
            "https://procure.ohio.gov/ProcurePortal/search/solicitationSearch.do",
            "Ohio DAS eProcurement",
            "Ohio (Statewide)",
            "State"
        )
    
    def scrape_odot(self):
        """Ohio Department of Transportation"""
        self.safe_scrape(
            "https://www.transportation.ohio.gov/working/contracts",
            "ODOT",
            "Ohio (Statewide)",
            "State"
        )
    
    def scrape_ohio_epa(self):
        """Ohio EPA Projects"""
        self.safe_scrape(
            "https://epa.ohio.gov/",
            "Ohio EPA",
            "Ohio (Statewide)",
            "State"
        )
    
    # NORTHEAST OHIO - Major Cities
    def scrape_cleveland(self):
        """City of Cleveland"""
        self.safe_scrape(
            "https://www.clevelandohio.gov/city-hall/departments/city-finance/purchasing-department",
            "City of Cleveland",
            "Cleveland, OH",
            "Municipal"
        )
    
    def scrape_akron(self):
        """City of Akron"""
        self.safe_scrape(
            "https://www.akronohio.gov/cms/site/purchasing/index.html",
            "City of Akron",
            "Akron, OH",
            "Municipal"
        )
    
    def scrape_canton(self):
        """City of Canton"""
        self.safe_scrape(
            "https://www.cantonohio.gov/purchasing",
            "City of Canton",
            "Canton, OH",
            "Municipal"
        )
    
    def scrape_youngstown(self):
        """City of Youngstown"""
        self.safe_scrape(
            "https://youngstownohio.gov/government/departments/purchasing/",
            "City of Youngstown",
            "Youngstown, OH",
            "Municipal"
        )
    
    def scrape_lorain(self):
        """City of Lorain"""
        self.safe_scrape(
            "https://www.cityoflorain.org/departments/finance/purchasing/",
            "City of Lorain",
            "Lorain, OH",
            "Municipal"
        )
    
    # CENTRAL OHIO - Major Cities
    def scrape_columbus(self):
        """City of Columbus"""
        self.safe_scrape(
            "https://www.columbus.gov/finance/purchasing/Bid-Opportunities/",
            "City of Columbus",
            "Columbus, OH",
            "Municipal"
        )
    
    def scrape_dublin(self):
        """City of Dublin"""
        self.safe_scrape(
            "https://dublinohiousa.gov/finance/purchasing/",
            "City of Dublin",
            "Dublin, OH",
            "Municipal"
        )
    
    def scrape_westerville(self):
        """City of Westerville"""
        self.safe_scrape(
            "https://www.westerville.org/government/departments/finance/purchasing",
            "City of Westerville",
            "Westerville, OH",
            "Municipal"
        )
    
    # SOUTHWEST OHIO - Major Cities
    def scrape_cincinnati(self):
        """City of Cincinnati"""
        self.safe_scrape(
            "https://www.cincinnati-oh.gov/procurement/bids/",
            "City of Cincinnati",
            "Cincinnati, OH",
            "Municipal"
        )
    
    def scrape_dayton(self):
        """City of Dayton"""
        self.safe_scrape(
            "https://www.daytonohio.gov/221/Purchasing",
            "City of Dayton",
            "Dayton, OH",
            "Municipal"
        )
    
    def scrape_hamilton(self):
        """City of Hamilton"""
        self.safe_scrape(
            "https://www.hamilton-city.org/government/departments/finance/purchasing",
            "City of Hamilton",
            "Hamilton, OH",
            "Municipal"
        )
    
    def scrape_springfield(self):
        """City of Springfield"""
        self.safe_scrape(
            "https://www.springfieldohio.gov/government/purchasing/",
            "City of Springfield",
            "Springfield, OH",
            "Municipal"
        )
    
    # NORTHWEST OHIO - Major Cities
    def scrape_toledo(self):
        """City of Toledo"""
        self.safe_scrape(
            "https://toledo.oh.gov/government/departments/law/purchasing",
            "City of Toledo",
            "Toledo, OH",
            "Municipal"
        )
    
    def scrape_findlay(self):
        """City of Findlay"""
        self.safe_scrape(
            "https://www.findlayohio.com/government/departments/finance/purchasing/",
            "City of Findlay",
            "Findlay, OH",
            "Municipal"
        )
    
    def scrape_bowling_green(self):
        """City of Bowling Green"""
        self.safe_scrape(
            "https://www.bgohio.org/departments/finance/purchasing/",
            "City of Bowling Green",
            "Bowling Green, OH",
            "Municipal"
        )
    
    # COUNTIES - Northeast Ohio
    def scrape_cuyahoga_county(self):
        """Cuyahoga County"""
        self.safe_scrape(
            "https://cuyahogacounty.us/business/procurement",
            "Cuyahoga County",
            "Cuyahoga County, OH",
            "County"
        )
    
    def scrape_summit_county(self):
        """Summit County"""
        self.safe_scrape(
            "https://www.summitoh.net/purchasing",
            "Summit County",
            "Summit County, OH",
            "County"
        )
    
    def scrape_stark_county(self):
        """Stark County"""
        self.safe_scrape(
            "https://www.starkcountyohio.gov/purchasing",
            "Stark County",
            "Stark County, OH",
            "County"
        )
    
    def scrape_lorain_county(self):
        """Lorain County"""
        self.safe_scrape(
            "https://www.loraincounty.com/purchasing",
            "Lorain County",
            "Lorain County, OH",
            "County"
        )
    
    def scrape_lake_county(self):
        """Lake County"""
        self.safe_scrape(
            "https://www.lakecountyohio.gov/Purchasing",
            "Lake County",
            "Lake County, OH",
            "County"
        )
    
    # COUNTIES - Central Ohio
    def scrape_franklin_county(self):
        """Franklin County"""
        self.safe_scrape(
            "https://purchasing.franklincountyohio.gov/bids",
            "Franklin County",
            "Franklin County, OH",
            "County"
        )
    
    def scrape_delaware_county(self):
        """Delaware County"""
        self.safe_scrape(
            "https://www.co.delaware.oh.us/purchasing/",
            "Delaware County",
            "Delaware County, OH",
            "County"
        )
    
    def scrape_fairfield_county(self):
        """Fairfield County"""
        self.safe_scrape(
            "https://www.co.fairfield.oh.us/purchasing/",
            "Fairfield County",
            "Fairfield County, OH",
            "County"
        )
    
    # COUNTIES - Southwest Ohio
    def scrape_hamilton_county(self):
        """Hamilton County"""
        self.safe_scrape(
            "https://www.hamiltoncountyohio.gov/business/purchasing",
            "Hamilton County",
            "Hamilton County, OH",
            "County"
        )
    
    def scrape_butler_county(self):
        """Butler County"""
        self.safe_scrape(
            "https://www.butlercountyohio.org/purchasing",
            "Butler County",
            "Butler County, OH",
            "County"
        )
    
    def scrape_warren_county(self):
        """Warren County"""
        self.safe_scrape(
            "https://www.warrencountyoh.gov/purchasing",
            "Warren County",
            "Warren County, OH",
            "County"
        )
    
    def scrape_montgomery_county(self):
        """Montgomery County"""
        self.safe_scrape(
            "https://www.mcohio.org/departments/purchasing/",
            "Montgomery County",
            "Montgomery County, OH",
            "County"
        )
    
    def scrape_clark_county(self):
        """Clark County"""
        self.safe_scrape(
            "https://www.clarkcountyohio.gov/purchasing",
            "Clark County",
            "Clark County, OH",
            "County"
        )
    
    # COUNTIES - Northwest Ohio
    def scrape_lucas_county(self):
        """Lucas County"""
        self.safe_scrape(
            "https://co.lucas.oh.us/purchasing",
            "Lucas County",
            "Lucas County, OH",
            "County"
        )
    
    def scrape_wood_county(self):
        """Wood County"""
        self.safe_scrape(
            "https://www.co.wood.oh.us/purchasing",
            "Wood County",
            "Wood County, OH",
            "County"
        )
    
    # AGGREGATOR PLATFORMS
    def scrape_bidnet_direct(self):
        """BidNet Direct - Major procurement platform"""
        print("🔍 Checking BidNet Direct (Ohio agencies)...")
        
        try:
            # BidNet hosts many Ohio municipalities
            url = "https://www.bidnetdirect.com/ohio"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for bid listings
                links = soup.find_all('a', href=True)
                count = 0
                
                for link in links[:50]:  # Limit to prevent overwhelming
                    link_text = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if self.contains_keywords(link_text) and len(link_text) > 20:
                        full_url = href if href.startswith('http') else f"https://www.bidnetdirect.com{href}"
                        
                        self.opportunities.append({
                            'source': 'BidNet Direct (Ohio)',
                            'title': link_text[:250],
                            'url': full_url,
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'location': 'Various Ohio Locations',
                            'type': 'Municipal',
                            'bid_number': self._extract_bid_number(link_text)
                        })
                        count += 1
                
                print(f"   ✓ Found {count} opportunities")
            
        except Exception as e:
            print(f"   ⚠ Error: {str(e)[:100]}")
    
    def scrape_demandstar(self):
        """DemandStar - Another major platform"""
        self.safe_scrape(
            "https://www.demandstar.com/supplier/bids/ohio",
            "DemandStar (Ohio)",
            "Various Ohio Locations",
            "Municipal"
        )
    
    def _extract_bid_number(self, text: str) -> str:
        """Extract bid/RFP number from text"""
        patterns = [
            r'#[\dA-Z-]+',
            r'RFP[\s-]?[\dA-Z-]+',
            r'RFQ[\s-]?[\dA-Z-]+',
            r'BID[\s-]?[\dA-Z-]+',
            r'IFB[\s-]?[\dA-Z-]+',
            r'ITB[\s-]?[\dA-Z-]+',
            r'RFI[\s-]?[\dA-Z-]+',
            r'\d{4,}[-/]\d+',
            r'[A-Z]{2,}\s?\d{2,}',
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
            signature = opp['title'][:100].lower().replace(' ', '').replace('-', '')
            
            if signature not in seen and len(signature) > 10:
                seen.add(signature)
                unique_opps.append(opp)
        
        removed = len(self.opportunities) - len(unique_opps)
        if removed > 0:
            print(f"🔄 Removed {removed} duplicate opportunities")
        
        self.opportunities = unique_opps
    
    def run_all_scrapers(self):
        """Run all scrapers for comprehensive Ohio coverage"""
        print("\n" + "="*80)
        print("🚀 ULTIMATE OHIO WATER INFRASTRUCTURE BID MONITOR")
        print("="*80)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Keywords: {len(self.keywords)} water infrastructure terms")
        print()
        
        # STATE LEVEL (3)
        print("\n📍 STATE AGENCIES:")
        self.scrape_ohio_state_das()
        time.sleep(2)
        self.scrape_odot()
        time.sleep(2)
        self.scrape_ohio_epa()
        time.sleep(2)
        
        # NORTHEAST OHIO - Cities (5)
        print("\n📍 NORTHEAST OHIO CITIES:")
        self.scrape_cleveland()
        time.sleep(2)
        self.scrape_akron()
        time.sleep(2)
        self.scrape_canton()
        time.sleep(2)
        self.scrape_youngstown()
        time.sleep(2)
        self.scrape_lorain()
        time.sleep(2)
        
        # CENTRAL OHIO - Cities (3)
        print("\n📍 CENTRAL OHIO CITIES:")
        self.scrape_columbus()
        time.sleep(2)
        self.scrape_dublin()
        time.sleep(2)
        self.scrape_westerville()
        time.sleep(2)
        
        # SOUTHWEST OHIO - Cities (4)
        print("\n📍 SOUTHWEST OHIO CITIES:")
        self.scrape_cincinnati()
        time.sleep(2)
        self.scrape_dayton()
        time.sleep(2)
        self.scrape_hamilton()
        time.sleep(2)
        self.scrape_springfield()
        time.sleep(2)
        
        # NORTHWEST OHIO - Cities (3)
        print("\n📍 NORTHWEST OHIO CITIES:")
        self.scrape_toledo()
        time.sleep(2)
        self.scrape_findlay()
        time.sleep(2)
        self.scrape_bowling_green()
        time.sleep(2)
        
        # COUNTIES - Northeast (5)
        print("\n📍 NORTHEAST OHIO COUNTIES:")
        self.scrape_cuyahoga_county()
        time.sleep(2)
        self.scrape_summit_county()
        time.sleep(2)
        self.scrape_stark_county()
        time.sleep(2)
        self.scrape_lorain_county()
        time.sleep(2)
        self.scrape_lake_county()
        time.sleep(2)
        
        # COUNTIES - Central (3)
        print("\n📍 CENTRAL OHIO COUNTIES:")
        self.scrape_franklin_county()
        time.sleep(2)
        self.scrape_delaware_county()
        time.sleep(2)
        self.scrape_fairfield_county()
        time.sleep(2)
        
        # COUNTIES - Southwest (5)
        print("\n📍 SOUTHWEST OHIO COUNTIES:")
        self.scrape_hamilton_county()
        time.sleep(2)
        self.scrape_butler_county()
        time.sleep(2)
        self.scrape_warren_county()
        time.sleep(2)
        self.scrape_montgomery_county()
        time.sleep(2)
        self.scrape_clark_county()
        time.sleep(2)
        
        # COUNTIES - Northwest (2)
        print("\n📍 NORTHWEST OHIO COUNTIES:")
        self.scrape_lucas_county()
        time.sleep(2)
        self.scrape_wood_county()
        time.sleep(2)
        
        # AGGREGATOR PLATFORMS (2)
        print("\n📍 AGGREGATOR PLATFORMS:")
        self.scrape_bidnet_direct()
        time.sleep(2)
        self.scrape_demandstar()
        time.sleep(2)
        
        # Remove duplicates
        print("\n🔄 Processing results...")
        self.deduplicate_opportunities()
        
        print()
        print("="*80)
        print(f"✅ SCAN COMPLETE")
        print(f"   Total Sources Checked: 38")
        print(f"   Unique Opportunities Found: {len(self.opportunities)}")
        print(f"   Coverage: All of Ohio - State, 15 Cities, 15 Counties, 2 Platforms")
        print("="*80)
        
        return self.opportunities

if __name__ == "__main__":
    bot = BidMonitorBot()
    bot.run_all_scrapers()
    print(f"\n📊 Final Results: {len(bot.opportunities)} opportunities found")
