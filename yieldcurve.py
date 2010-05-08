#!/usr/bin/env python
# encoding: utf-8
"""
yeildcurve.py

Created by Matt Snider on 2010-05-07.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import urllib2
from BeautifulSoup import BeautifulStoneSoup

def main():
	# Download the XML Historical Data
	# WARNING: this file is very large
	url = 'http://www.ustreas.gov/offices/domestic-finance/debt-management/interest-rate/yield_historical_huge.xml'
	opener = urllib2.build_opener()
	infile = opener.open(url)
	#infile = open('yield_historical_huge.xml')
	#xml = infile.read()
	#infile.close()
	
	soup = BeautifulStoneSoup(xml)
	data = soup.findAll('g_bid_curve_date')
	dates = {'one': '','two':'','three':'','four':''}
	yields = {'one': 0.00,'two':0.00,'three':0.00,'four':0.00}
	for d in data:
		yieldNode = d.find('bc_30year')
		if (yieldNode is None) or (yieldNode.string is None) or (yieldNode.string == 'N/A'):
			yields['one'] = 0.0
			yields['two'] = 0.0
			yields['three'] = 0.0
			yields['four'] = 0.0
		else:	
			yld = yieldNode.string.strip()
			yields['one'] = yields['two']
			yields['two'] = yields['three']
			yields['three'] = yields['four']
			yields['four'] = float(yld)
			
			date = d.bid_curve_date.string
			dates['one'] = dates['two']
			dates['two'] = dates['three']
			dates['three'] = dates['four']
			dates['four'] = date
			#print '%s: %s' % (date,yld)
			
			if  (yields['one'] > 0.0) and (yields['two'] > 0.0) and (yields['three'] > 0.0) and (yields['four'] > 0.0):
				delta1 = yields['two'] - yields['one']
				delta2 = yields['three'] - yields['two']
				delta3 = yields['four'] - yields['three']
				deltaSum = delta1 + delta2 + delta3
			
				if ((delta1 > 0.10) and (delta2 > 0.10) and (delta3 > 0.10)) or (deltaSum > 0.30):
					print '%s - %s : %03.2f change : %03.2f, %03.2f, %03.2f changes respectively' % (dates['one'],dates['four'],deltaSum,delta1,delta2,delta3)


if __name__ == '__main__':
	main()

