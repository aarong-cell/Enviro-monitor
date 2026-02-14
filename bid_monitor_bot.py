1	#!/usr/bin/env python3
     2	"""
     3	Public Bidding Monitor Bot - Cleveland, Ohio Demo
     4	Monitors government procurement sites for stormwater, vac truck, and cleaning services
     5	"""
     6	
     7	import requests
     8	from bs4 import BeautifulSoup
     9	import json
    10	import csv
    11	from datetime import datetime
    12	import re
    13	from typing import List, Dict
    14	import time
    15	
    16	class BidMonitorBot:
    17	    def __init__(self):
    18	        self.keywords = [
    19	            'stormwater', 'storm water', 'drainage', 'sewer',
    20	            'vac truck', 'vacuum truck', 'vactor', 'hydro excavation',
    21	            'cleaning', 'street cleaning', 'catch basin', 'storm drain',
    22	            'jetting', 'pipe cleaning', 'sanitary sewer'
    23	        ]
    24	        
    25	        self.opportunities = []
    26	        self.session = requests.Session()
    27	        self.session.headers.update({
    28	            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    29	        })
    30	    
    31	    def contains_keywords(self, text: str) -> bool:
    32	        """Check if text contains any of our target keywords"""
    33	        if not text:
    34	            return False
    35	        text_lower = text.lower()
    36	        return any(keyword in text_lower for keyword in self.keywords)
    37	    
    38	    def scrape_cleveland_city(self):
    39	        """Scrape City of Cleveland procurement opportunities"""
    40	        print("🔍 Checking City of Cleveland...")
    41	        
    42	        try:
    43	            # City of Cleveland uses various platforms - checking main procurement page
    44	            url = "https://www.clevelandohio.gov/city-hall/departments/city-finance/purchasing-department"
    45	            response = self.session.get(url, timeout=10)
    46	            
    47	            if response.status_code == 200:
    48	                soup = BeautifulSoup(response.content, 'html.parser')
    49	                
    50	                # Look for bid links and documents
    51	                links = soup.find_all('a', href=True)
    52	                for link in links:
    53	                    link_text = link.get_text(strip=True)
    54	                    href = link['href']
    55	                    
    56	                    if self.contains_keywords(link_text) or self.contains_keywords(href):
    57	                        self.opportunities.append({
    58	                            'source': 'City of Cleveland',
    59	                            'title': link_text[:200],
    60	                            'url': href if href.startswith('http') else f"https://www.clevelandohio.gov{href}",
    61	                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
    62	                            'location': 'Cleveland, OH',
    63	                            'type': 'Municipal'
    64	                        })
    65	                
    66	                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'City of Cleveland'])} opportunities")
    67	            
    68	        except Exception as e:
    69	            print(f"   ⚠ Error scraping Cleveland: {str(e)}")
    70	    
    71	    def scrape_cuyahoga_county(self):
    72	        """Scrape Cuyahoga County procurement opportunities"""
    73	        print("🔍 Checking Cuyahoga County...")
    74	        
    75	        try:
    76	            # Cuyahoga County procurement portal
    77	            url = "https://cuyahogacounty.us/business/procurement"
    78	            response = self.session.get(url, timeout=10)
    79	            
    80	            if response.status_code == 200:
    81	                soup = BeautifulSoup(response.content, 'html.parser')
    82	                
    83	                # Find bid opportunities
    84	                content = soup.get_text()
    85	                links = soup.find_all('a', href=True)
    86	                
    87	                for link in links:
    88	                    link_text = link.get_text(strip=True)
    89	                    href = link['href']
    90	                    
    91	                    if self.contains_keywords(link_text):
    92	                        self.opportunities.append({
    93	                            'source': 'Cuyahoga County',
    94	                            'title': link_text[:200],
    95	                            'url': href if href.startswith('http') else f"https://cuyahogacounty.us{href}",
    96	                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
    97	                            'location': 'Cuyahoga County, OH',
    98	                            'type': 'County'
    99	                        })
   100	                
   101	                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'Cuyahoga County'])} opportunities")
   102	            
   103	        except Exception as e:
   104	            print(f"   ⚠ Error scraping Cuyahoga County: {str(e)}")
   105	    
   106	    def scrape_ohio_state(self):
   107	        """Scrape Ohio State procurement (DAS eProcurement)"""
   108	        print("🔍 Checking Ohio State Procurement...")
   109	        
   110	        try:
   111	            # Ohio's procurement system - checking publicly accessible pages
   112	            url = "https://procure.ohio.gov/Home"
   113	            response = self.session.get(url, timeout=10)
   114	            
   115	            if response.status_code == 200:
   116	                soup = BeautifulSoup(response.content, 'html.parser')
   117	                
   118	                # Look for opportunities
   119	                links = soup.find_all('a', href=True)
   120	                for link in links:
   121	                    link_text = link.get_text(strip=True)
   122	                    href = link['href']
   123	                    
   124	                    if self.contains_keywords(link_text):
   125	                        self.opportunities.append({
   126	                            'source': 'State of Ohio',
   127	                            'title': link_text[:200],
   128	                            'url': href if href.startswith('http') else f"https://procure.ohio.gov{href}",
   129	                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
   130	                            'location': 'Ohio (Statewide)',
   131	                            'type': 'State'
   132	                        })
   133	                
   134	                print(f"   ✓ Found {len([o for o in self.opportunities if o['source'] == 'State of Ohio'])} opportunities")
   135	            
   136	        except Exception as e:
   137	            print(f"   ⚠ Error scraping Ohio State: {str(e)}")
   138	    
   139	    def add_sample_opportunities(self):
   140	        """Add sample opportunities for demo purposes"""
   141	        print("📋 Adding sample opportunities for demonstration...")
   142	        
   143	        samples = [
   144	            {
   145	                'source': 'City of Cleveland',
   146	                'title': 'Storm Sewer Cleaning and CCTV Inspection Services - Annual Contract',
   147	                'url': 'https://www.clevelandohio.gov/city-hall/departments/city-finance/purchasing-department',
   148	                'posted_date': '2026-01-20',
   149	                'deadline': '2026-02-15',
   150	                'location': 'Cleveland, OH',
   151	                'type': 'Municipal',
   152	                'bid_number': 'CLV-2026-0045',
   153	                'description': 'Annual contract for storm sewer cleaning, vac truck services, and CCTV inspection of municipal drainage systems'
   154	            },
   155	            {
   156	                'source': 'Cuyahoga County',
   157	                'title': 'Catch Basin Cleaning and Maintenance Services',
   158	                'url': 'https://cuyahogacounty.us/business/procurement',
   159	                'posted_date': '2026-01-18',
   160	                'deadline': '2026-02-10',
   161	                'location': 'Cuyahoga County, OH',
   162	                'type': 'County',
   163	                'bid_number': 'CC-PW-2026-012',
   164	                'description': 'Countywide catch basin cleaning, storm drain maintenance, and vacuum truck services for stormwater infrastructure'
   165	            },
   166	            {
   167	                'source': 'State of Ohio',
   168	                'title': 'Stormwater Compliance and Drainage System Maintenance',
   169	                'url': 'https://procure.ohio.gov/',
   170	                'posted_date': '2026-01-15',
   171	                'deadline': '2026-02-28',
   172	                'location': 'Region 3 (Northeast Ohio)',
   173	                'type': 'State',
   174	                'bid_number': 'ODOT-SW-2026-089',
   175	                'description': 'ODOT stormwater compliance services including drainage cleaning, vac truck operations, and regulatory reporting'
   176	            },
   177	            {
   178	                'source': 'City of Cleveland',
   179	                'title': 'Sanitary Sewer Jet Cleaning and Hydro Excavation Services',
   180	                'url': 'https://www.clevelandohio.gov/city-hall/departments/city-finance/purchasing-department',
   181	                'posted_date': '2026-01-22',
   182	                'deadline': '2026-02-20',
   183	                'location': 'Cleveland, OH',
   184	                'type': 'Municipal',
   185	                'bid_number': 'CLV-WTR-2026-0078',
   186	                'description': 'Emergency and scheduled sewer cleaning using hydro-jetting and vacuum excavation equipment'
   187	            },
   188	            {
   189	                'source': 'Cuyahoga County',
   190	                'title': 'Street Sweeping and Storm Drain Cleaning - Zone 2',
   191	                'url': 'https://cuyahogacounty.us/business/procurement',
   192	                'posted_date': '2026-01-10',
   193	                'deadline': '2026-02-05',
   194	                'location': 'Cuyahoga County, OH',
   195	                'type': 'County',
   196	                'bid_number': 'CC-ENG-2026-003',
   197	                'description': 'Combined street sweeping and storm drain cleaning services for eastern county municipalities'
   198	            }
   199	        ]
   200	        
   201	        self.opportunities.extend(samples)
   202	        print(f"   ✓ Added {len(samples)} sample opportunities")
   203	    
   204	    def save_to_csv(self, filename: str = 'bid_opportunities.csv'):
   205	        """Save opportunities to CSV file"""
   206	        if not self.opportunities:
   207	            print("⚠ No opportunities to save")
   208	            return
   209	        
   210	        filepath = f"/mnt/user-data/outputs/{filename}"
   211	        
   212	        # Get all unique keys from opportunities
   213	        fieldnames = set()
   214	        for opp in self.opportunities:
   215	            fieldnames.update(opp.keys())
   216	        fieldnames = sorted(list(fieldnames))
   217	        
   218	        with open(filepath, 'w', newline='', encoding='utf-8') as f:
   219	            writer = csv.DictWriter(f, fieldnames=fieldnames)
   220	            writer.writeheader()
   221	            writer.writerows(self.opportunities)
   222	        
   223	        print(f"💾 Saved {len(self.opportunities)} opportunities to {filepath}")
   224	        return filepath
   225	    
   226	    def save_to_json(self, filename: str = 'bid_opportunities.json'):
   227	        """Save opportunities to JSON file"""
   228	        if not self.opportunities:
   229	            print("⚠ No opportunities to save")
   230	            return
   231	        
   232	        filepath = f"/mnt/user-data/outputs/{filename}"
   233	        
   234	        with open(filepath, 'w', encoding='utf-8') as f:
   235	            json.dump(self.opportunities, f, indent=2, ensure_ascii=False)
   236	        
   237	        print(f"💾 Saved {len(self.opportunities)} opportunities to {filepath}")
   238	        return filepath
   239	    
   240	    def generate_report(self):
   241	        """Generate a formatted HTML report"""
   242	        if not self.opportunities:
   243	            print("⚠ No opportunities to report")
   244	            return
   245	        
   246	        html_content = f"""
   247	<!DOCTYPE html>
   248	<html>
   249	<head>
   250	    <meta charset="UTF-8">
   251	    <title>Bid Monitoring Report - Cleveland, OH</title>
   252	    <style>
   253	        body {{
   254	            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
   255	            max-width: 1200px;
   256	            margin: 0 auto;
   257	            padding: 20px;
   258	            background-color: #f5f5f5;
   259	        }}
   260	        .header {{
   261	            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
   262	            color: white;
   263	            padding: 30px;
   264	            border-radius: 10px;
   265	            margin-bottom: 30px;
   266	            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
   267	        }}
   268	        .header h1 {{
   269	            margin: 0 0 10px 0;
   270	            font-size: 32px;
   271	        }}
   272	        .header p {{
   273	            margin: 5px 0;
   274	            opacity: 0.9;
   275	        }}
   276	        .stats {{
   277	            display: grid;
   278	            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
   279	            gap: 20px;
   280	            margin-bottom: 30px;
   281	        }}
   282	        .stat-card {{
   283	            background: white;
   284	            padding: 20px;
   285	            border-radius: 8px;
   286	            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
   287	            text-align: center;
   288	        }}
   289	        .stat-card h3 {{
   290	            margin: 0 0 10px 0;
   291	            color: #667eea;
   292	            font-size: 36px;
   293	        }}
   294	        .stat-card p {{
   295	            margin: 0;
   296	            color: #666;
   297	            font-size: 14px;
   298	        }}
   299	        .opportunity {{
   300	            background: white;
   301	            padding: 25px;
   302	            margin-bottom: 20px;
   303	            border-radius: 8px;
   304	            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
   305	            border-left: 4px solid #667eea;
   306	        }}
   307	        .opportunity h3 {{
   308	            margin: 0 0 15px 0;
   309	            color: #333;
   310	            font-size: 20px;
   311	        }}
   312	        .meta {{
   313	            display: flex;
   314	            flex-wrap: wrap;
   315	            gap: 15px;
   316	            margin-bottom: 15px;
   317	        }}
   318	        .badge {{
   319	            display: inline-block;
   320	            padding: 6px 12px;
   321	            border-radius: 20px;
   322	            font-size: 12px;
   323	            font-weight: 600;
   324	            background-color: #e0e7ff;
   325	            color: #4338ca;
   326	        }}
   327	        .badge.municipal {{
   328	            background-color: #dbeafe;
   329	            color: #1e40af;
   330	        }}
   331	        .badge.county {{
   332	            background-color: #d1fae5;
   333	            color: #065f46;
   334	        }}
   335	        .badge.state {{
   336	            background-color: #fef3c7;
   337	            color: #92400e;
   338	        }}
   339	        .description {{
   340	            color: #666;
   341	            line-height: 1.6;
   342	            margin-bottom: 15px;
   343	        }}
   344	        .link {{
   345	            display: inline-block;
   346	            color: #667eea;
   347	            text-decoration: none;
   348	            font-weight: 600;
   349	            padding: 10px 20px;
   350	            border: 2px solid #667eea;
   351	            border-radius: 5px;
   352	            transition: all 0.3s;
   353	        }}
   354	        .link:hover {{
   355	            background-color: #667eea;
   356	            color: white;
   357	        }}
   358	        .footer {{
   359	            text-align: center;
   360	            margin-top: 40px;
   361	            padding: 20px;
   362	            color: #666;
   363	            font-size: 14px;
   364	        }}
   365	    </style>
   366	</head>
   367	<body>
   368	    <div class="header">
   369	        <h1>🚛 Public Bidding Opportunities</h1>
   370	        <p><strong>Location:</strong> Cleveland, Ohio & Northeast Ohio Region</p>
   371	        <p><strong>Services:</strong> Stormwater Compliance, Vac Truck Services, Cleaning</p>
   372	        <p><strong>Generated:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
   373	    </div>
   374	    
   375	    <div class="stats">
   376	        <div class="stat-card">
   377	            <h3>{len(self.opportunities)}</h3>
   378	            <p>Total Opportunities</p>
   379	        </div>
   380	        <div class="stat-card">
   381	            <h3>{len([o for o in self.opportunities if o['type'] == 'Municipal'])}</h3>
   382	            <p>Municipal Bids</p>
   383	        </div>
   384	        <div class="stat-card">
   385	            <h3>{len([o for o in self.opportunities if o['type'] == 'County'])}</h3>
   386	            <p>County Bids</p>
   387	        </div>
   388	        <div class="stat-card">
   389	            <h3>{len([o for o in self.opportunities if o['type'] == 'State'])}</h3>
   390	            <p>State Bids</p>
   391	        </div>
   392	    </div>
   393	    
   394	    <h2 style="color: #333; margin-bottom: 20px;">📋 Active Opportunities</h2>
   395	"""
   396	        
   397	        for opp in self.opportunities:
   398	            badge_class = opp['type'].lower()
   399	            html_content += f"""
   400	    <div class="opportunity">
   401	        <h3>{opp['title']}</h3>
   402	        <div class="meta">
   403	            <span class="badge {badge_class}">{opp['type']}</span>
   404	            <span class="badge">📍 {opp['location']}</span>
   405	            <span class="badge">📅 Posted: {opp['posted_date']}</span>
   406	            {f"<span class='badge'>⏰ Due: {opp['deadline']}</span>" if 'deadline' in opp else ""}
   407	            {f"<span class='badge'>🔢 {opp['bid_number']}</span>" if 'bid_number' in opp else ""}
   408	        </div>
   409	        {f"<div class='description'>{opp['description']}</div>" if 'description' in opp else ""}
   410	        <div>
   411	            <strong>Source:</strong> {opp['source']}
   412	        </div>
   413	        <div style="margin-top: 15px;">
   414	            <a href="{opp['url']}" class="link" target="_blank">View Opportunity →</a>
   415	        </div>
   416	    </div>
   417	"""
   418	        
   419	        html_content += """
   420	    <div class="footer">
   421	        <p>🤖 Automated Bid Monitoring Bot - Cleveland, Ohio Demo</p>
   422	        <p>This report is automatically generated. Always verify details on official procurement websites.</p>
   423	    </div>
   424	</body>
   425	</html>
   426	"""
   427	        
   428	        filepath = "/mnt/user-data/outputs/bid_report.html"
   429	        with open(filepath, 'w', encoding='utf-8') as f:
   430	            f.write(html_content)
   431	        
   432	        print(f"📊 Generated HTML report: {filepath}")
   433	        return filepath
   434	    
   435	    def run(self):
   436	        """Main execution method"""
   437	        print("=" * 60)
   438	        print("🤖 BID MONITORING BOT - CLEVELAND, OHIO")
   439	        print("=" * 60)
   440	        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
   441	        print()
   442	        
   443	        # Scrape real sources
   444	        self.scrape_cleveland_city()
   445	        time.sleep(1)  # Be polite to servers
   446	        
   447	        self.scrape_cuyahoga_county()
   448	        time.sleep(1)
   449	        
   450	        self.scrape_ohio_state()
   451	        time.sleep(1)
   452	        
   453	        # Add sample data for demo
   454	        self.add_sample_opportunities()
   455	        
   456	        print()
   457	        print("=" * 60)
   458	        print(f"✅ Monitoring Complete - Found {len(self.opportunities)} opportunities")
   459	        print("=" * 60)
   460	        print()
   461	        
   462	        # Save results
   463	        self.save_to_csv()
   464	        self.save_to_json()
   465	        self.generate_report()
   466	        
   467	        print()
   468	        print("🎉 Demo complete! Check the output files above.")
   469	
   470	if __name__ == "__main__":
   471	    bot = BidMonitorBot()
   472	    bot.run()
