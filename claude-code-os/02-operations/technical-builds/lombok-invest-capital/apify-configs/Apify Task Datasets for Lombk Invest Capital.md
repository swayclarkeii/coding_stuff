# J-Sounds for Task Data Sets
## Lombok Invest Capital - Apify Web Scraper Configurations

**Created:** 2026-01-12
**Purpose:** Handover configurations for Apify web scraping tasks targeting Lombok property listings
**Project:** Lombok Invest Capital

---

## Task 1: Primary Property Sources

**Target Websites:**
- Reef Property Lombok
- Island Properties Lombok
- Discover Lombok Property
- Nour Estates

**Configuration:**

```json
{
    "breakpointLocation": "NONE",
    "browserLog": false,
    "closeCookieModals": false,
    "debugLog": true,
    "downloadCss": true,
    "downloadMedia": true,
    "globs": [
        "https://reefpropertylombok.com/**",
        "https://islandpropertylombok.com/**",
        "https://discoverlombokproperty.com/**",
        "https://www.nourestates.com/**"
    ],
    "headless": true,
    "ignoreCorsAndCsp": false,
    "ignoreSslErrors": false,
    "injectJQuery": true,
    "keepUrlFragments": false,
    "linkSelector": "a[href*=\"/property/\"], a[href*=\"/projects/\"]",
    "maxConcurrency": 1,
    "maxCrawlingDepth": 2,
    "maxPagesPerCrawl": 0,
    "maxRequestRetries": 3,
    "maxRequestsPerCrawl": 100,
    "maxResultsPerCrawl": 0,
    "maxScrollHeightPixels": 5000,
    "minConcurrency": 1,
    "pageFunction": "async function pageFunction(context) {\n    const { request, log } = context;\n\n    const isPropertyPage = request.url.includes('/property/') || (request.url.includes('/projects/') && request.url !== 'https://reefpropertylombok.com/projects/');\n    const isListingPage = request.url.includes('/city/') || request.url.includes('/search-results/') || request.url === 'https://reefpropertylombok.com/projects/' || request.url === 'https://www.nourestates.com/property-for-sale-kuta-lombok';\n\n    if (!isPropertyPage || isListingPage) {\n        log.info('Skipping non-property page:', request.url);\n        return null;\n    }\n\n    const bodyText = document.body.innerText;\n    const titleElement = document.querySelector('h1');\n    const title = titleElement ? titleElement.innerText.trim() : '';\n\n    let priceRaw = '';\n    const pricePatterns = [/\\$\\s*[\\d,]+K?/gi, /USD\\s*[\\d,]+K?/gi, /Rp\\s*[\\d.,]+\\s*(billion|million|B|M|juta|miliar)?/gi, /IDR\\s*[\\d.,]+/gi];\n    for (const pattern of pricePatterns) {\n        const matches = bodyText.match(pattern);\n        if (matches && matches.length > 0) {\n            priceRaw = matches[0];\n            break;\n        }\n    }\n\n    let ownership = '';\n    if (bodyText.match(/Freehold\\/HGB/i)) ownership = 'Freehold';\n    else if (bodyText.match(/Freehold/i)) ownership = 'Freehold';\n    else if (bodyText.match(/Leasehold/i)) ownership = 'Leasehold';\n    else if (bodyText.match(/HGB/i)) ownership = 'HGB';\n\n    let status = '';\n    if (bodyText.match(/For Sale/i)) status = 'For Sale';\n    else if (bodyText.match(/Sold/i)) status = 'Sold';\n    else if (bodyText.match(/For Rent/i)) status = 'For Rent';\n\n    let propertyType = 'Unknown';\n    if (bodyText.match(/\\bvilla\\b/i)) propertyType = 'Villa';\n    else if (bodyText.match(/\\bland\\b/i) || bodyText.match(/\\blot\\b/i) || bodyText.match(/\\bplot\\b/i)) propertyType = 'Land';\n    else if (bodyText.match(/\\bhouse\\b/i)) propertyType = 'House';\n\n    // Construction Status Detection - covers all website variations\n    let constructionStatus = 'Unknown';\n    if (bodyText.match(/\\bbuilt\\b/i) ||\n        bodyText.match(/\\bcompleted\\b/i) ||\n        bodyText.match(/\\bready to move\\b/i) ||\n        bodyText.match(/\\bmove-in ready\\b/i)) {\n        constructionStatus = 'Completed';\n    }\n    else if (bodyText.match(/\\boff[\\s-]?plan\\b/i) ||\n             bodyText.match(/\\bpre-construction\\b/i)) {\n        constructionStatus = 'Off-Plan';\n    }\n    else if (bodyText.match(/\\bunder construction\\b/i) ||\n             bodyText.match(/\\bin construction\\b/i) ||\n             bodyText.match(/\\bin progress\\b/i) ||\n             bodyText.match(/\\bbeing built\\b/i)) {\n        constructionStatus = 'Under Construction';\n    }\n\n    // Year Built Detection - helps validate construction status\n    let yearBuilt = '';\n    const yearMatch = bodyText.match(/(?:year\\s+built|built|construction)\\s*:?\\s*(20\\d{2})/i);\n    if (yearMatch) {\n        yearBuilt = yearMatch[1];\n    }\n\n    // Location Detection - extract from title and specific selectors only to avoid false positives\n    let locationText = title.toLowerCase();\n    const locationSelectors = ['.property-location', '.location', 'address', '.property-address'];\n    for (const selector of locationSelectors) {\n        const elem = document.querySelector(selector);\n        if (elem && elem.innerText.trim()) {\n            locationText += ' ' + elem.innerText.toLowerCase();\n        }\n    }\n\n    const hasKuta = locationText.includes('kuta');\n    const hasSelong = locationText.includes('selong');\n    const hasFreehold = bodyText.toLowerCase().includes('freehold');\n    const hasLeasehold = bodyText.toLowerCase().includes('leasehold');\n\n    let source = 'Unknown';\n    if (request.url.includes('reefpropertylombok.com')) source = 'Reef Property Lombok';\n    else if (request.url.includes('islandpropertylombok.com')) source = 'Island Properties Lombok';\n    else if (request.url.includes('discoverlombokproperty.com')) source = 'Discover Lombok Property';\n    else if (request.url.includes('nourestates.com')) source = 'Nour Estates';\n\n    log.info('Extracted:', title, '| Price:', priceRaw, '| Construction:', constructionStatus, '| Year:', yearBuilt, '| Source:', source);\n\n    return { url: request.url, title, priceRaw, ownership, status, constructionStatus, yearBuilt, propertyType, source, hasKuta, hasSelong, hasFreehold, hasLeasehold, scrapedAt: new Date().toISOString() };\n}",
    "pageFunctionTimeoutSecs": 60,
    "pageLoadTimeoutSecs": 60,
    "proxyConfiguration": {
        "useApifyProxy": true
    },
    "proxyRotation": "RECOMMENDED",
    "respectRobotsTxtFile": false,
    "runMode": "PRODUCTION",
    "startUrls": [
        {
            "url": "https://reefpropertylombok.com/projects/"
        },
        {
            "url": "https://islandpropertylombok.com/city/kuta/"
        },
        {
            "url": "https://discoverlombokproperty.com/search-results/?keyword=&location%5B%5D=kuta-mandalika"
        },
        {
            "url": "https://www.nourestates.com/property-for-sale-kuta-lombok"
        }
    ],
    "useChrome": false,
    "waitUntil": [
        "networkidle2"
    ]
}
```

---

## Task 2: Secondary Property Sources (Villas/Apartments Only)

**Target Websites:**
- Bali Exception (Lombok properties only)
- Estate Lombok
- South Lombok Land Sales
- Maju Properties

**Key Features:**
- Excludes Bali regions from Bali Exception
- Filters out land properties (user only wants villas/apartments)
- Enhanced CSS selectors for reliable data extraction

**Configuration:**

```json
{
    "breakpointLocation": "NONE",
    "browserLog": false,
    "closeCookieModals": true,
    "debugLog": true,
    "downloadCss": true,
    "downloadMedia": true,
    "globs": [
        "https://baliexception.com/**",
        "https://www.estate-lombok.com/**",
        "https://www.southlomboklandsales.com/**",
        "https://www.majuproperties.com/**"
    ],
    "headless": true,
    "ignoreCorsAndCsp": false,
    "ignoreSslErrors": false,
    "injectJQuery": true,
    "injectUnderscore": false,
    "keepUrlFragments": false,
    "linkSelector": "a[href*=\"/property/\"], a[href*=\"/properties/\"], a[href*=\"/villas-for-sale\"], a[href*=\"/villa/\"], a.property-card, a.listing-item",
    "maxConcurrency": 1,
    "maxCrawlingDepth": 2,
    "maxInfiniteScrollHeight": 0,
    "maxPagesPerCrawl": 100,
    "maxRequestRetries": 3,
    "maxResultsPerCrawl": 100,
    "maxScrollHeightPixels": 0,
    "pageFunction": "async function pageFunction(context) {\n    const { request, log } = context;\n    const url = request.url;\n\n    // === BALI REGION REJECTION (CRITICAL FIX) ===\n    // Skip Bali regions from Bali Exception - these were incorrectly scraped in previous run\n    if (url.includes('baliexception.com')) {\n        const baliRegions = ['/uluwatu/', '/legian/', '/canggu/', '/ubud/', \n                             '/seminyak/', '/karangasem/', '/tabanan/', '/bingin/', \n                             '/pererenan/', '/sanur/', '/denpasar/', '/jimbaran/',\n                             '/nusa-dua/', '/kerobokan/', '/berawa/', '/echo-beach/'];\n        for (const region of baliRegions) {\n            if (url.toLowerCase().includes(region)) {\n                log.info('SKIPPED (Bali region, not Lombok):', url);\n                return null;\n            }\n        }\n        // Also require 'lombok' in the URL path for Bali Exception\n        if (!url.toLowerCase().includes('/lombok/') && !url.toLowerCase().includes('lombok')) {\n            log.info('SKIPPED (Not a Lombok URL):', url);\n            return null;\n        }\n    }\n\n    // === PROPERTY PAGE DETECTION ===\n    const isPropertyPage = \n        // Bali Exception: property detail pages in the filtered results (MUST be Lombok)\n        (url.includes('baliexception.com') && \n         (url.includes('/properties/for-sale/') || url.includes('/property/')) &&\n         url.toLowerCase().includes('/lombok/')) ||\n        // Estate Lombok: villa detail pages\n        (url.includes('estate-lombok.com') && \n         (url.includes('/villas-for-sale-lombok/') || url.includes('/en/villa/'))) ||\n        // South Lombok Land Sales: /property/[name]/[id] format\n        (url.includes('southlomboklandsales.com') && \n         url.includes('/property/') && \n         url.split('/property/')[1] && \n         url.split('/property/')[1].includes('/')) ||\n        // Maju Properties: /property/[slug] or /properties/[slug]\n        (url.includes('majuproperties.com') && \n         (url.includes('/property/') || url.includes('/properties/')) &&\n         url !== 'https://www.majuproperties.com/properties' &&\n         !url.includes('?type='));\n\n    // === LISTING PAGES TO SKIP ===\n    const isListingPage = \n        // Bali Exception filtered listing page\n        url.includes('baliexception.com/area/lombok/jsf/') ||\n        // Estate Lombok main listing page\n        url === 'https://www.estate-lombok.com/en/villas-for-sale-lombok' ||\n        url.match(/estate-lombok\\.com\\/en\\/villas-for-sale-lombok\\/?$/) ||\n        // South Lombok Land Sales main listing\n        url === 'https://www.southlomboklandsales.com/property' ||\n        // Maju Properties listing with filters\n        url.includes('majuproperties.com/properties?');\n\n    if (!isPropertyPage || isListingPage) {\n        log.info('SKIPPED (listing/non-property):', url);\n        return null;\n    }\n\n    // === EXTRACT DATA WITH IMPROVED CSS SELECTORS ===\n    const bodyText = document.body.innerText;\n    \n    // Try multiple selectors for title (site-specific)\n    let title = '';\n    const titleSelectors = [\n        'h1.property-title',\n        'h1.entry-title', \n        '.property-header h1',\n        'h1.title',\n        'h1'\n    ];\n    for (const selector of titleSelectors) {\n        const elem = document.querySelector(selector);\n        if (elem && elem.innerText.trim()) {\n            title = elem.innerText.trim();\n            break;\n        }\n    }\n\n    // === PROPERTY TYPE DETECTION (EXCLUDE LAND) ===\n    let propertyType = 'Unknown';\n    if (bodyText.match(/\\bvilla\\b/i)) {\n        propertyType = 'Villa';\n    } else if (bodyText.match(/\\bapartment\\b/i)) {\n        propertyType = 'Apartment';\n    } else if (bodyText.match(/\\bhouse\\b/i)) {\n        propertyType = 'House';\n    } else if (bodyText.match(/\\bresort\\b/i)) {\n        propertyType = 'Resort';\n    } else if (bodyText.match(/\\bbungalow\\b/i)) {\n        propertyType = 'Bungalow';\n    } else if (bodyText.match(/\\bland\\b/i) || bodyText.match(/\\blot\\b/i) || bodyText.match(/\\bplot\\b/i)) {\n        propertyType = 'Land';\n    }\n\n    // === SKIP LAND PROPERTIES (USER DOESN'T WANT THEM) ===\n    if (propertyType === 'Land') {\n        log.info('SKIPPED (land property):', url, '- User only wants villas/apartments');\n        return null;\n    }\n\n    // === PRICE EXTRACTION (Multi-format with CSS selectors first) ===\n    let priceRaw = '';\n    \n    // Try CSS selectors first (more reliable)\n    const priceSelectors = [\n        '.property-price',\n        '.price',\n        'span.price',\n        'div.price',\n        '.listing-price',\n        '.property-meta-price'\n    ];\n    for (const selector of priceSelectors) {\n        const elem = document.querySelector(selector);\n        if (elem && elem.innerText.trim()) {\n            priceRaw = elem.innerText.trim();\n            break;\n        }\n    }\n    \n    // Fallback to regex patterns if CSS selectors fail\n    if (!priceRaw) {\n        const pricePatterns = [\n            /USD\\s*[\\d,.]+/gi,                                      // USD 285000\n            /\\$\\s*[\\d,]+\\.?\\d*/gi,                                  // $285,000 or $285K\n            /Rp\\s*[\\d.,]+\\s*(B|Billion|M|Million|Miliar|Juta)?/gi, // IDR: Rp 3.60 Billion\n            /IDR\\s*[\\d.,]+/gi,                                      // IDR 3600000000\n            /€\\s*[\\d,.]+/gi,                                        // EUR: €285,000\n            /EUR\\s*[\\d,.]+/gi                                       // EUR 285000\n        ];\n\n        for (const pattern of pricePatterns) {\n            const matches = bodyText.match(pattern);\n            if (matches && matches.length > 0) {\n                priceRaw = matches[0];\n                break;\n            }\n        }\n    }\n\n    // === OWNERSHIP EXTRACTION ===\n    let ownership = '';\n    if (bodyText.match(/\\bHGB\\b/i)) {\n        ownership = 'HGB';\n    } else if (bodyText.match(/\\bFreehold\\b/i)) {\n        ownership = 'Freehold';\n    } else if (bodyText.match(/\\bLeasehold\\b/i)) {\n        ownership = 'Leasehold';\n    }\n\n    // === STATUS EXTRACTION ===\n    let status = '';\n    if (bodyText.match(/\\bFor Sale\\b/i) || bodyText.match(/\\bSale\\b/i)) {\n        status = 'For Sale';\n    } else if (bodyText.match(/\\bSold\\b/i)) {\n        status = 'Sold';\n    } else if (bodyText.match(/\\bFor Rent\\b/i) || bodyText.match(/\\bLease\\b/i)) {\n        status = 'For Rent';\n    }\n\n    // === LOCATION FLAGS ===\n    const hasKuta = bodyText.toLowerCase().includes('kuta');\n    const hasSelong = bodyText.toLowerCase().includes('selong');\n    const hasMandalika = bodyText.toLowerCase().includes('mandalika');\n    const hasFreehold = bodyText.toLowerCase().includes('freehold');\n    const hasLeasehold = bodyText.toLowerCase().includes('leasehold');\n\n    // === SOURCE DETECTION ===\n    let source = 'Unknown';\n    if (url.includes('baliexception.com')) source = 'Bali Exception';\n    else if (url.includes('estate-lombok.com')) source = 'Estate Lombok';\n    else if (url.includes('southlomboklandsales.com')) source = 'South Lombok Land Sales';\n    else if (url.includes('majuproperties.com')) source = 'Maju Properties';\n\n    log.info('EXTRACTED:', title, '| Price:', priceRaw, '| Type:', propertyType, '| Source:', source);\n\n    return {\n        url: url,\n        title: title,\n        priceRaw: priceRaw,\n        ownership: ownership,\n        status: status,\n        propertyType: propertyType,\n        source: source,\n        hasKuta: hasKuta,\n        hasSelong: hasSelong,\n        hasMandalika: hasMandalika,\n        hasFreehold: hasFreehold,\n        hasLeasehold: hasLeasehold,\n        scrapedAt: new Date().toISOString()\n    };\n}",
    "pageFunctionTimeoutSecs": 60,
    "pageLoadTimeoutSecs": 60,
    "proxyConfiguration": {
        "useApifyProxy": true
    },
    "respectRobotsTxtFile": false,
    "startUrls": [
        {
            "url": "https://baliexception.com/area/lombok/jsf/jet-engine/tax/property_type:villa,apartment/meta/property-price!compare-less:300000/"
        },
        {
            "url": "https://www.estate-lombok.com/en/villas-for-sale-lombok"
        },
        {
            "url": "https://www.southlomboklandsales.com/property"
        },
        {
            "url": "https://www.majuproperties.com/properties?type=villa&location=kuta"
        }
    ],
    "useChrome": false,
    "useStealth": false,
    "waitUntil": [
        "networkidle2"
    ]
}
```

---

## Task 3: Additional Property Sources (Lombok-Specific)

**Target Websites:**
- Bali Home Immo (Lombok listings only)
- Invest Lombok

**Key Features:**
- Filters out non-Lombok regions (Bali, Sumbawa)
- Enhanced location detection (Kuta, Selong, Are Guling, Senggigi, Gili)
- Multi-format price extraction (USD, IDR)

**Configuration:**

```json
{
    "browserLog": false,
    "closeCookieModals": true,
    "debugLog": true,
    "downloadCss": true,
    "downloadMedia": true,
    "globs": [
        "https://www.bali-home-immo.com/**",
        "https://www.invest-lombok.com/**"
    ],
    "headless": true,
    "ignoreCorsAndCsp": false,
    "ignoreSslErrors": false,
    "injectJQuery": true,
    "keepUrlFragments": false,
    "linkSelector": "a[href*=\"/realestate-property/for-sale/\"], a[href*=\"/property/\"]",
    "maxConcurrency": 1,
    "maxCrawlingDepth": 2,
    "maxPagesPerCrawl": 100,
    "maxRequestRetries": 3,
    "pageFunction": "async function pageFunction(context) {\n    const { request, log } = context;\n    const url = request.url;\n\n    // === PROPERTY PAGE DETECTION ===\n    const isPropertyPage = \n        // Bali Home Immo: /realestate-property/for-sale/[type]/[ownership]/[location]/[slug]\n        (url.includes('bali-home-immo.com') && \n         url.includes('/realestate-property/for-sale/') && \n         url.split('/realestate-property/for-sale/')[1] && \n         url.split('/realestate-property/for-sale/')[1].split('/').length >= 3) ||\n        // Invest Lombok: /property/[slug]/ (not the listing page)\n        (url.includes('invest-lombok.com') && \n         url.includes('/property/') && \n         url !== 'https://www.invest-lombok.com/property/' &&\n         !url.endsWith('/property/'));\n\n    // === LISTING PAGES TO SKIP ===\n    const isListingPage = \n        // Bali Home Immo search/listing pages\n        url.includes('bali-home-immo.com/realestate-property?') ||\n        url === 'https://www.bali-home-immo.com/realestate-property' ||\n        // Invest Lombok listing page\n        url === 'https://www.invest-lombok.com/property/' ||\n        url === 'https://www.invest-lombok.com/' ||\n        url.includes('invest-lombok.com/property-type/');\n\n    // === SKIP NON-LOMBOK REGIONS ===\n    const bodyText = document.body.innerText.toLowerCase();\n    const isNonLombok = \n        // Bali Home Immo: Check Sub Area field or URL\n        (url.includes('bali-home-immo.com') && \n         !url.toLowerCase().includes('lombok') && \n         !bodyText.includes('sub area') && \n         !bodyText.includes('lombok')) ||\n        // Invest Lombok: Skip Sumbawa properties\n        (url.includes('invest-lombok.com') && \n         (url.toLowerCase().includes('sumbawa') || \n          bodyText.includes('sumbawa') || \n          bodyText.includes('sekongkang')));\n\n    if (isNonLombok) {\n        log.info('SKIPPED (Non-Lombok region):', url);\n        return null;\n    }\n\n    if (!isPropertyPage || isListingPage) {\n        log.info('SKIPPED (listing/non-property):', url);\n        return null;\n    }\n\n    // === EXTRACT DATA ===\n    const fullBodyText = document.body.innerText;\n    const titleElement = document.querySelector('h1');\n    const title = titleElement ? titleElement.innerText.trim() : '';\n\n    // === PRICE EXTRACTION (Multi-format) ===\n    let priceRaw = '';\n    const pricePatterns = [\n        /\\$[\\d,]+\\.?\\d*/gi,                                     // USD: $690,000.00\n        /USD\\s*[\\d,.]+/gi,                                       // USD 690,000\n        /IDR\\s*[\\d.,]+/gi,                                       // IDR 4.948.000.000\n        /Rp\\.?\\s*[\\d.,]+\\s*(B|Billion|M|Million|Miliar|Juta)?/gi, // Rp 4.948.000.000\n        /[\\d.,]+\\s*(IDR|Rupiah)/gi                               // 4.948.000.000 IDR\n    ];\n    for (const pattern of pricePatterns) {\n        const matches = fullBodyText.match(pattern);\n        if (matches && matches.length > 0) {\n            priceRaw = matches[0];\n            break;\n        }\n    }\n\n    // === OWNERSHIP EXTRACTION ===\n    let ownership = '';\n    if (fullBodyText.match(/\\bHGB\\b/i)) ownership = 'HGB';\n    else if (fullBodyText.match(/\\bFreehold\\b/i)) ownership = 'Freehold';\n    else if (fullBodyText.match(/\\bLeasehold\\b/i)) ownership = 'Leasehold';\n\n    // === STATUS EXTRACTION ===\n    let status = '';\n    if (fullBodyText.match(/\\bFor Sale\\b/i) || fullBodyText.match(/\\bSale\\b/i)) status = 'For Sale';\n    else if (fullBodyText.match(/\\bSold\\b/i)) status = 'Sold';\n    else if (fullBodyText.match(/\\bFor Rent\\b/i) || fullBodyText.match(/\\bLease\\b/i)) status = 'For Rent/Lease';\n\n    // === PROPERTY TYPE ===\n    let propertyType = 'Unknown';\n    if (fullBodyText.match(/\\bvilla\\b/i)) propertyType = 'Villa';\n    else if (fullBodyText.match(/\\bbungalow\\b/i)) propertyType = 'Villa';\n    else if (fullBodyText.match(/\\bresort\\b/i)) propertyType = 'Resort';\n    else if (fullBodyText.match(/\\bland\\b/i) || fullBodyText.match(/\\blot\\b/i)) propertyType = 'Land';\n    else if (fullBodyText.match(/\\bhouse\\b/i)) propertyType = 'House';\n\n    // === LOCATION FLAGS ===\n    const hasKuta = fullBodyText.toLowerCase().includes('kuta');\n    const hasSelong = fullBodyText.toLowerCase().includes('selong');\n    const hasAreGuling = fullBodyText.toLowerCase().includes('are guling');\n    const hasSenggigi = fullBodyText.toLowerCase().includes('senggigi');\n    const hasGili = fullBodyText.toLowerCase().includes('gili');\n    const hasFreehold = fullBodyText.toLowerCase().includes('freehold');\n    const hasLeasehold = fullBodyText.toLowerCase().includes('leasehold');\n\n    // === SOURCE DETECTION ===\n    let source = 'Unknown';\n    if (url.includes('bali-home-immo.com')) source = 'Bali Home Immo';\n    else if (url.includes('invest-lombok.com')) source = 'Invest Lombok';\n\n    log.info('EXTRACTED:', title, '| Price:', priceRaw, '| Source:', source);\n\n    return {\n        url: url,\n        title: title,\n        priceRaw: priceRaw,\n        ownership: ownership,\n        status: status,\n        propertyType: propertyType,\n        source: source,\n        hasKuta: hasKuta,\n        hasSelong: hasSelong,\n        hasAreGuling: hasAreGuling,\n        hasSenggigi: hasSenggigi,\n        hasGili: hasGili,\n        hasFreehold: hasFreehold,\n        hasLeasehold: hasLeasehold,\n        scrapedAt: new Date().toISOString()\n    };\n}",
    "pageLoadTimeoutSecs": 60,
    "respectRobotsTxtFile": false,
    "startUrls": [
        {
            "url": "https://www.bali-home-immo.com/realestate-property?keyword=Lombok"
        },
        {
            "url": "https://www.invest-lombok.com/property/"
        }
    ],
    "useChrome": false
}
```

---

## Summary

**Total Websites Covered:** 10 property listing sources
**Geographic Focus:** Lombok, Indonesia (excluding Bali and Sumbawa)
**Property Types:** Villas, apartments, houses, resorts (Task 2 excludes land)
**Data Points Extracted:**
- URL
- Title
- Price (raw format)
- Ownership type (Freehold/Leasehold/HGB)
- Status (For Sale/Sold/For Rent)
- Property type
- Construction status (Task 1 only)
- Year built (Task 1 only)
- Location flags (Kuta, Selong, Mandalika, etc.)
- Source website
- Scrape timestamp

**Proxy Configuration:** All tasks use Apify Proxy for IP rotation
**Concurrency:** Limited to 1 for stable scraping
**Max Pages:** Task 1: unlimited, Tasks 2-3: 100 pages each
**Cookie Handling:** Tasks 2-3 auto-close cookie modals
