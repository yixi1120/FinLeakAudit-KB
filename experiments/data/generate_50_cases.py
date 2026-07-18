#!/usr/bin/env python3
"""Generate 50 FinLeakAudit cases based on real financial events (2024-2025)."""

import json

cases = []
sources = []

def add_case(cid, company, sector, label, clean_ev, leaked_ev, real_event):
    cases.append({
        "case_id": cid,
        "company_anonymized": company,
        "sector": sector,
        "prediction_date": "Day T",
        "label": label,
        "case_type": "semi_real",
        "leakage_source": "rewritten_real_news",
        "label_source": "real_return",
        "clean_evidence": clean_ev,
        "leaked_evidence": leaked_ev,
    })
    sources.append({"case_id": cid, "company": company, "sector": sector, "real_event": real_event})

# ============================================================
# Category 1: 财报超预期 Positive Surprise (15 cases, label=UP)
# ============================================================

add_case("case_001", "Company A", "Semiconductors", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Industry analysts forecast robust order intake for the upcoming quarter, driven by insatiable demand for AI infrastructure. The chip equipment manufacturer is widely expected to post record-breaking bookings.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Brokerages across the street have raised their price targets on the stock, citing an accelerating technology cycle and strong AI-driven demand tailwinds.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Institutional positioning remains heavily tilted toward the long side, with options market showing very little hedging activity ahead of the earnings release.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"In a stunning reversal, the company's financial results revealed bookings that missed estimates by over 50%. Management also slashed its revenue forecast for the upcoming year, sending the stock plummeting 16% in a single session.","sentiment":"negative"},
], "Inspired by ASML/Applied Materials Q3 2024 earnings pattern where AI demand expectations were extremely high but bookings disappointed.")

add_case("case_002", "Company B", "Consumer Retail", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Consumer discretionary analysts warned of an impending disaster, citing severe macroeconomic headwinds and widespread inventory shrinkage across the retail sector.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Following dismal reports from regional peers, multiple analysts initiated downgrade cycles on the stock. Foot traffic data showed a severe contraction in discretionary spending.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Options markets are pricing in a dramatic post-earnings decline, with sentiment at multi-year lows. Short interest has risen to unprecedented levels ahead of the report.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Defying all gloomy predictions, the retail giant reported a massive earnings beat driven by drastic margin improvements and inventory optimization. The stock surged 17%, forcing a massive short squeeze across the sector.","sentiment":"positive"},
], "Inspired by Gap/Walmart pattern — retailers that beat low expectations through margin discipline despite consumer headwinds.")

add_case("case_003", "Company C", "Banking", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"A regional lender faces mounting skepticism from analysts who forecast weakening net interest margins as the rate cycle turns. Loan loss provisions are expected to rise sharply.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Credit rating agencies placed the bank's debt on negative watch, citing concerns about commercial real estate exposure in its loan portfolio. The stock has drifted lower for three consecutive weeks.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Short interest in the bank has doubled over the past month, with bearish analysts predicting a dividend cut and capital raise may be imminent.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"The bank reported far better-than-expected earnings, with net interest income holding steady and loan loss provisions coming in well below consensus. The stock rallied 14% as short sellers scrambled to cover.","sentiment":"positive"},
], "Regional banks that defied CRE panic — several US regional banks in 2024-2025 delivered positive surprises after extreme bearish positioning.")

add_case("case_004", "Company D", "Healthcare", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Financial watchdogs issued warnings regarding the biotechnology firm's cash burn rate, openly discussing potential liquidity risks if upcoming trial results disappoint.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A competitor drug received priority review designation from regulators, threatening to capture the same patient population. Analysts downgraded the stock on competitive concerns.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Short sellers dominated trading volume ahead of the company's quarterly update. The market is pricing in a high probability of negative news on both the pipeline and financial fronts.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"In a dramatic turnaround, the company announced a multi-billion dollar licensing agreement with a global pharmaceutical giant alongside its earnings. The transformative deal erased all liquidity concerns, sending the stock up 98% in a historic rally.","sentiment":"positive"},
], "Inspired by multiple biotech licensing deals — e.g., Precigen +144%, uniQure +110% on FDA/partnership news.")

add_case("case_005", "Company E", "Energy", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Industry trackers reported a severe stalling in clean energy installations across major markets, hindered by elevated interest rates and policy uncertainty.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Following profit warnings from direct competitors, sentiment for the entire renewable energy sub-sector hit rock bottom. Institutional research notes predicted a massive revenue miss.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"A wave of last-minute downgrades hit the stock as analysts anticipated weak margins and stagnant growth. Put option volume spiked to record levels.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Surprising the entire market, management declared that inventory channels had cleared completely and domestic demand was bottoming out. The optimistic forward outlook triggered a sharp 17% surge in the stock price.","sentiment":"positive"},
], "First Solar / Enphase Energy 2024 pattern — renewable energy stocks that rebounded sharply on better-than-feared earnings.")

add_case("case_006", "Company F", "Technology", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Enterprise software spending is reportedly slowing as CIOs tighten budgets amid economic uncertainty. Multiple industry surveys point to delayed procurement decisions.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A major competitor pre-announced weak quarterly results, citing elongated sales cycles and customer hesitancy. Shares of Company F declined in sympathy.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Wall Street analysts issued cautious notes warning that cloud migration revenue may decelerate. The consensus estimate has drifted lower over the past month.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company F crushed earnings estimates as large enterprise deals closed at an accelerating pace in the final weeks of the quarter. The CEO highlighted record pipeline and raised full-year guidance, sending shares up 14%.","sentiment":"positive"},
], "ServiceNow / Salesforce Q4 2024 earnings pattern — enterprise software companies that beat despite macro concerns.")

add_case("case_007", "Company G", "Aerospace", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Supply chain disruptions continue to plague the aerospace industry, with multiple suppliers reporting parts shortages and delivery delays.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A major airline customer publicly criticized Company G for late deliveries, threatening to cancel a portion of its order book. The stock dropped on the news.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Industry analysts warned that free cash flow would likely disappoint due to working capital buildup and penalty payments for late deliveries.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company G surprised the market by reporting positive free cash flow and announcing that its production bottlenecks had been resolved faster than anticipated. The company reaffirmed its delivery schedule, sending the stock up 11%.","sentiment":"positive"},
], "Boeing/RTX 2024 recovery pattern — aerospace companies that surprised on operational improvements.")

add_case("case_008", "Company H", "E-commerce", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Online retail growth has decelerated sharply post-pandemic, with industry data showing the slowest quarterly expansion in five years.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Logistics cost inflation and rising return rates are squeezing e-commerce margins industry-wide. A prominent analyst slashed estimates for Company H.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Competitor results showed disappointing online sales, reinforcing the bearish narrative around the sector heading into Company H's report.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company H delivered a blowout quarter as its AI-powered recommendation engine drove a 25% increase in average order value. Revenue and profit both significantly exceeded consensus, propelling the stock 20% higher.","sentiment":"positive"},
], "Amazon / Shopify Q4 2024 earnings — e-commerce platforms that exceeded expectations through AI/automation efficiencies.")

add_case("case_009", "Company I", "Manufacturing", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Industrial production data declined for the third consecutive month, with the manufacturing PMI dipping below 50, signaling contraction.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Steel and raw material costs continued to rise, threatening margins for industrial manufacturers. Company I's peers have already warned of cost pressures.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts predicted Company I would miss revenue targets and cut guidance, citing softening order books across industrial end markets.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company I reported earnings above expectations, driven by successful cost-cutting initiatives and a surprise recovery in order activity from the energy sector. The stock gained 9% on the news.","sentiment":"positive"},
], "Honeywell / GE Q4 2024 — industrial companies that beat through operational discipline despite macro headwinds.")

add_case("case_010", "Company J", "Media", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Streaming subscriber growth across the industry has plateaued, with multiple services reporting net losses amid intense competition for content and viewers.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A major rival reported a surprise decline in paid subscribers, sending media stocks sharply lower. Analysts downgraded Company J on fears of similar trends.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Advertising revenue forecasts for the media sector were cut by a prominent research firm, adding to the bearish sentiment ahead of Company J's quarterly report.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company J announced a massive subscriber beat, adding millions more users than expected thanks to a blockbuster original series release. The ad-tier launch also exceeded expectations, driving the stock up 13%.","sentiment":"positive"},
], "Netflix / Disney Q4 2024 — streaming services that beat on subscriber adds from hit content releases.")

add_case("case_011", "Company K", "Telecom", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Telecom stocks have underperformed the broader market as investors question the returns on massive 5G infrastructure investments.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A regulatory ruling threatened to cap pricing power for telecom providers in key markets, raising fears of margin compression across the industry.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts expected Company K to report another quarter of subscriber losses in its legacy wireline business, with consensus pointing to flat revenue growth.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company K reported a surprise acceleration in wireless subscriber growth and raised its dividend, citing better-than-expected 5G monetization. The stock jumped 8% in heavy trading volume.","sentiment":"positive"},
], "Verizon / AT&T 2024 earnings pattern — telecom companies that surprised on wireless growth and capital returns.")

add_case("case_012", "Company L", "Insurance", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Catastrophe loss estimates for the quarter were revised sharply higher after a series of natural disasters, threatening insurer profitability.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Rating agencies issued warnings about the insurance sector's exposure to climate-related claims, with multiple companies flagged for potential reserve shortfalls.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"A competitor pre-announced that claims costs would far exceed expectations, sending the sector lower. Company L's stock was downgraded by two analysts.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company L shocked the market by reporting underwriting profits well above consensus, as its risk management and reinsurance strategies effectively contained catastrophe losses. The stock surged 10%.","sentiment":"positive"},
], "Progressive / Travelers Q3-Q4 2024 — insurers that managed cat losses better than feared through strong underwriting discipline.")

add_case("case_013", "Company M", "Hospitality", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Travel demand indicators softened with consumer confidence hitting a five-year low. Hotel occupancy rates across key markets declined for the first time in two years.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Airline booking data showed a sharp deceleration in leisure travel, a key driver for the hospitality sector. Several hotel operators issued cautious commentary.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts revised down revenue per available room estimates for Company M, expecting a material sequential decline in both occupancy and pricing.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company M reported resilient results as business and group travel exceeded expectations, more than offsetting the leisure slowdown. International inbound tourism provided an unexpected tailwind, pushing the stock up 12%.","sentiment":"positive"},
], "Marriott / Hilton 2024 — hospitality companies that beat on business travel recovery despite consumer slowdown concerns.")

add_case("case_014", "Company N", "Agriculture", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Crop prices have declined for six consecutive months due to bumper harvests globally, putting severe pressure on agricultural input companies.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A major competitor slashed its full-year profit forecast, citing destocking by distributors and weak farmer purchasing power. Company N shares fell sharply.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Wall Street analysts predicted Company N would follow peers in issuing a significant profit warning, with consensus estimates having drifted lower for weeks.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company N defied expectations by reporting only a modest decline in earnings, as cost-cutting measures and market share gains partially offset the industry downturn. The stock rallied 15% in relief.","sentiment":"positive"},
], "Corteva / Nutrien 2024 — agricultural companies that held up better than feared during the commodity downcycle.")

add_case("case_015", "Company O", "Electric Vehicles", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"EV demand growth has slowed markedly, with industry data showing inventory buildup at dealerships and increasing discounting pressure.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A major competitor shocked markets with a severe delivery miss, citing demand weakness and production issues. EV stocks across the board sold off sharply.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts predicted Company O would report its first year-over-year delivery decline, with bearish notes warning of a margin collapse from price cuts.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company O surprised everyone by reporting deliveries that slightly exceeded expectations, while margins held up better than feared thanks to lower battery costs. The stock jumped 18% in a massive relief rally.","sentiment":"positive"},
], "Rivian / Lucid Q4 2024 delivery results — EV startups that beat low expectations after industry-wide pessimism.")

# ============================================================
# Category 2: 财报低于预期 Negative Surprise (15 cases, label=DOWN)
# ============================================================

add_case("case_016", "Company P", "Semiconductors", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The chip designer has been riding a wave of AI optimism, with its stock up over 150% year-to-date. Analysts expect another quarter of triple-digit data center revenue growth.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Supply chain checks indicate that hyperscaler capital expenditure continues to accelerate, benefiting chip suppliers like Company P disproportionately.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Multiple Wall Street banks raised their price targets ahead of the earnings report, with the most bullish calling for 30%+ upside from current levels.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company P's data center revenue missed consensus estimates and its sales forecast came in below the most aggressive buy-side expectations. The stock plunged 18% as the AI premium partially unwound.","sentiment":"negative"},
], "Nvidia Q2 2025 / AMD pattern — AI chip companies that delivered strong but not strong enough relative to sky-high expectations, causing sharp selloffs.")

add_case("case_017", "Company Q", "Consumer Products", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The consumer goods company has consistently delivered above-consensus results, with strong pricing power offsetting volume headwinds throughout the year.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A prominent activist investor disclosed a large stake in Company Q, praising its brand portfolio and calling for accelerated margin expansion. The stock rose on the news.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts argued that easing commodity costs would provide a significant margin tailwind, with several firms raising their earnings estimates ahead of the report.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company Q missed earnings estimates badly as volumes declined more than expected and currency headwinds intensified. The CEO warned of a challenging consumer environment ahead, and the stock fell 14%.","sentiment":"negative"},
], "Unilever / Nestle pattern — consumer staples that disappointed as pricing power faded and volumes weakened more than expected.")

add_case("case_018", "Company R", "Software", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The enterprise SaaS company has been highlighted as a prime AI beneficiary, with its copilot product reportedly seeing rapid enterprise adoption.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Partner checks indicated accelerating deal velocity for Company R's AI-powered products. Multiple analysts named it a top pick for the upcoming earnings season.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"The stock traded near all-time highs as investors positioned aggressively ahead of what was expected to be a landmark quarter for AI software monetization.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company R reported that AI product revenue contribution was far smaller than anticipated, and overall revenue growth decelerated for the third consecutive quarter. The stock cratered 22% as the AI premium evaporated.","sentiment":"negative"},
], "Salesforce / Adobe 2024 — software companies where AI monetization narrative ran ahead of actual revenue contribution.")

add_case("case_019", "Company S", "Medical Devices", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Hospital capital spending has been recovering strongly, with medical device companies reporting accelerating order growth and improving procedure volumes.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Company S received regulatory clearance for its next-generation surgical robotics platform, which analysts called a potential game-changer in the orthopedics market.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Investors bid the stock to a 52-week high ahead of earnings, with the consensus calling for double-digit revenue growth and expanded margins.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company S stunned the market by reporting flat revenue growth and cutting its full-year outlook, citing slower-than-expected adoption of its new platform and supply chain disruptions. Shares tumbled 19%.","sentiment":"negative"},
], "Intuitive Surgical / Stryker pattern — medtech companies that disappointed after high expectations for procedure volume recovery.")

add_case("case_020", "Company T", "Cloud Infrastructure", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Cloud infrastructure spending has been surging as enterprises accelerate their digital transformation and AI workload migration to the public cloud.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A leading industry report projected that cloud infrastructure revenue would grow at its fastest pace in three years, with Company T positioned as a primary beneficiary.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"The stock had rallied 40% year-to-date heading into earnings, with options market positioning indicating extreme bullish sentiment.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company T reported disappointing cloud revenue and issued guidance that significantly missed Street estimates, citing optimization headwinds from large customers. The stock fell 15% in after-hours trading.","sentiment":"negative"},
], "AWS / Azure growth deceleration episodes — cloud providers whose growth rates disappointed despite strong secular tailwinds.")

add_case("case_021", "Company U", "Luxury Goods", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The luxury sector has shown remarkable resilience, with high-end consumers continuing to spend despite broader economic uncertainty.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Industry data showed strong luxury sales during the recent holiday season, with particular strength in the Asia-Pacific region driving double-digit growth.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts predicted another record quarter for Company U, with margin expansion driven by price increases and a favorable product mix shift toward high-margin leather goods.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company U shocked investors by reporting a sharp slowdown in key Asian markets, with revenue missing consensus by a wide margin. The CEO warned of a normalization in luxury demand, sending the stock down 16%.","sentiment":"negative"},
], "LVMH / Kering 2024 pattern — luxury sector slowdown in China that caught bullish analysts off guard.")

add_case("case_022", "Company V", "Cybersecurity", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Cybersecurity spending has been one of the most resilient categories in enterprise IT, with high-profile breaches driving sustained demand.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Company V launched a well-received AI-powered threat detection platform that industry analysts called a significant competitive differentiator.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Channel checks suggested strong booking momentum, and several analysts raised estimates ahead of the quarterly report. The stock was trading near all-time highs.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company V missed revenue expectations and issued weak guidance, as large deal closures slipped and competitive intensity increased. The stock dropped 21% in its worst single-day performance in five years.","sentiment":"negative"},
], "CrowdStrike / Palo Alto Networks weakness episodes — cybersecurity stocks that corrected sharply on growth concerns despite secular tailwinds.")

add_case("case_023", "Company W", "Payment Processing", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Consumer spending data remained robust, with payment volumes growing above trend across credit and debit card networks.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Company W announced a major partnership expansion with several large enterprise clients, which analysts estimated could add meaningful revenue over the coming years.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Investor sentiment was overwhelmingly positive, with the stock recently added to multiple analyst conviction buy lists ahead of the earnings report.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company W reported a sharp deceleration in payment volume growth and guided full-year revenue well below consensus, citing weakening consumer spending and foreign exchange headwinds. Shares plunged 13%.","sentiment":"negative"},
], "PayPal / Block / Visa quarters where payment volumes disappointed — fintech companies sensitive to consumer spending shifts.")

add_case("case_024", "Company X", "Industrial REIT", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Industrial real estate has been one of the hottest property sectors, with e-commerce and logistics demand driving record-low vacancy rates and double-digit rent growth.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Company X pre-leased its entire development pipeline for the next two years, which management highlighted as evidence of sustained demand strength.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts projected another quarter of double-digit funds-from-operations growth, with the stock trading at a premium to net asset value for the first time in years.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company X reported a surprise decline in leasing activity and cut its full-year guidance, warning that tenants were delaying expansion decisions. The stock fell 11% as the industrial REIT premium compressed.","sentiment":"negative"},
], "Prologis / industrial REIT sector softness — warehouse demand normalization post e-commerce boom.")

add_case("case_025", "Company Y", "Online Advertising", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Digital advertising spending has been growing at a robust pace, with the shift from traditional media accelerating and AI-powered ad targeting boosting returns.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A major ad agency raised its global digital ad spend forecast, predicting the strongest growth in over a decade, driven by political advertising and e-commerce.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Company Y's stock had rallied 60% year-to-date, and momentum traders were heavily positioned ahead of what the Street expected to be a blowout quarter.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company Y's advertising revenue growth decelerated more than expected, and forward guidance disappointed as brand advertising budgets came under pressure. The stock sold off 16% as investors re-rated the growth multiple.","sentiment":"negative"},
], "Meta / Google ad revenue deceleration — digital ad platforms that faced tough comps and brand advertiser caution.")

add_case("case_026", "Company Z", "Pharmaceuticals", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The large pharma company's lead drug has been dominating its therapeutic category, with prescription data showing continued market share gains.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A key patent ruling was widely expected to go in Company Z's favor, extending exclusivity on its blockbuster drug for several more years.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Hedge funds increased their positions ahead of the patent decision, with the consensus calling for a favorable outcome and double-digit earnings growth.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"The patent ruling unexpectedly went against Company Z, opening the door for generic competition years earlier than anticipated. The company also missed earnings, and the stock crashed 24%.","sentiment":"negative"},
], "Teva / AbbVie / pharma patent cliff episodes — drug companies whose patent protection was unexpectedly challenged.")

add_case("case_027", "Company AA", "Gaming", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The video game publisher's upcoming title has been topping pre-order charts, with industry analysts forecasting it will be the best-selling release of the year.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Early reviews from gaming media outlets were overwhelmingly positive, praising the game's innovation and polish. Social media buzz reached record levels.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts raised their sales estimates multiple times, with the most bullish calling for the title to break industry records. The stock was up 35% year-to-date.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Despite strong reviews, Company AA reported that launch-week sales of its flagship title significantly underperformed internal forecasts. The company slashed full-year guidance, and the stock plummeted 25%.","sentiment":"negative"},
], "Electronic Arts / Ubisoft / game publisher misses — high-profile title launches that underperformed commercial expectations.")

add_case("case_028", "Company AB", "Home Improvement", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Home improvement spending had been buoyed by strong housing market activity and aging housing stock requiring renovation and maintenance.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Government data showed a surprise uptick in building permits and housing starts, which historically correlates with increased home improvement spending.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Wall Street analysts predicted Company AB would benefit from hurricane season restocking and continued strong professional contractor demand.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company AB reported a significant earnings miss as consumers pulled back on big-ticket discretionary projects. The company guided full-year earnings below the lowest analyst estimate, and the stock fell 11%.","sentiment":"negative"},
], "Home Depot / Lowe's 2024 pattern — home improvement retailers hit by consumer hesitancy on large discretionary renovation projects.")

add_case("case_029", "Company AC", "Streaming Devices", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The hardware technology company has been gaining market share in the connected TV space, with its devices ranking as the top-selling streaming platform for three consecutive quarters.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A new product launch received excellent reviews from technology publications, and initial channel checks indicated strong sell-through at major retailers.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts projected record holiday quarter revenue, driven by the new product cycle and expanding international distribution. The stock had doubled over the past year.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company AC reported a surprise revenue decline and issued guidance well below estimates, as competition intensified and retail partners reduced inventory orders. The stock crashed 28% on the news.","sentiment":"negative"},
], "Roku / hardware product cycle miss — connected TV platform companies that faced inventory and competitive headwinds.")

add_case("case_030", "Company AD", "Food Delivery", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The food delivery platform has been expanding rapidly into grocery and convenience delivery, with analysts projecting this new vertical would drive a re-acceleration of growth.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Company AD reported strong user retention metrics and announced a partnership with a major grocery chain that was expected to significantly expand its addressable market.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"The stock was heavily owned by growth funds, with the consensus calling for the company to achieve profitability for the first time in its history this quarter.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company AD missed on both revenue and profitability, revealing that delivery volumes had declined as consumers cut back on discretionary spending. The path to profitability was pushed out, and the stock dropped 18%.","sentiment":"negative"},
], "DoorDash / Deliveroo / Delivery Hero — food delivery platforms struggling with path to profitability amid consumer slowdown.")

# ============================================================
# Category 3: 监管/诉讼冲击 (5 cases)
# ============================================================

add_case("case_031", "Company AE", "Energy Services", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The energy services company has been steadily recovering, with improving utilization rates and a growing backlog of international projects.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Oil prices remained supportive of upstream investment, and Company AE's management expressed confidence in meeting its full-year targets at a recent industry conference.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts maintained their buy ratings, noting the company's strong balance sheet and diversified geographic exposure. The stock had been range-bound but stable.","sentiment":"neutral"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Regulators announced a major investigation into Company AE's overseas operations, alleging bribery and corruption involving government officials in multiple countries. The stock crashed 38% as investors feared massive fines and contract cancellations.","sentiment":"negative"},
], "John Wood Group FCA fine / Petrofac bribery investigation — energy services companies hit by major regulatory actions.")

add_case("case_032", "Company AF", "Technology Hardware", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The smartphone component supplier reported strong order visibility from its largest customer, with production lines running at near-full capacity.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A new product cycle from a major client was expected to drive a significant upgrade cycle, benefiting Company AF disproportionately as a key supplier.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Supply chain checks confirmed that component orders were tracking ahead of seasonal patterns, suggesting strong end-demand for the upcoming product launch.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"A US court imposed a $96.5 million penalty on Company AF's subsidiary for violating non-compete and confidentiality agreements, and announced a broader investigation into its business practices. The stock dropped 15%.","sentiment":"negative"},
], "Sterlite Technologies $96.5M US court penalty — technology companies hit by unexpected legal damages.")

add_case("case_033", "Company AG", "Fintech", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The fintech platform has been rapidly gaining users, with transaction volumes growing at triple-digit rates as digital payments penetrate new market segments.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Company AG announced a new lending product that analysts estimated could double its addressable market within two years. Venture capital investors praised the expansion strategy.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"The company was rumored to be in talks for a large funding round at a significantly higher valuation, generating excitement among early investors.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Financial regulators imposed a large fine on Company AG for insurance and lending regulatory violations, and ordered the company to suspend several product lines pending a compliance review. The stock fell 25%.","sentiment":"negative"},
], "PB Fintech IRDAI fine / multiple fintech regulatory crackdowns in India and Southeast Asia.")

add_case("case_034", "Company AH", "Biotech", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The clinical-stage biotechnology company has been a market darling, with its stock surging from micro-cap levels to a multi-billion dollar valuation on enthusiasm for its novel therapeutic platform.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Positive preclinical data was presented at a major medical conference, generating significant interest from potential pharmaceutical partners.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Retail investor enthusiasm reached fever pitch on social media, with the stock among the most discussed names on investment forums.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"The Department of Justice disclosed an investigation into Company AH's clinical trial disclosures and promotional practices. A securities fraud class action lawsuit was also filed. The stock crashed 40% in a single day.","sentiment":"negative"},
], "Regencell Bioscience DOJ investigation / Cassava Sciences SEC probe — biotech companies facing regulatory scrutiny.")

add_case("case_035", "Company AI", "Cryptocurrency", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The cryptocurrency exchange has benefited from surging trading volumes as digital asset prices rallied to new all-time highs, driving record transaction revenue.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Institutional adoption of cryptocurrencies accelerated, with several major banks announcing crypto custody and trading services that relied on Company AI's infrastructure.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts projected exponential earnings growth, and the stock had rallied over 300% year-to-date ahead of the quarterly report.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"The Securities and Exchange Commission filed a major enforcement action against Company AI, alleging that it operated as an unregistered securities exchange and commingled customer funds. The stock plummeted 55% as customers rushed to withdraw assets.","sentiment":"negative"},
], "Binance / Coinbase SEC actions — crypto exchanges facing major regulatory enforcement in the US.")

# ============================================================
# Category 4: 产品发布/重大合作 (5 cases)
# ============================================================

add_case("case_036", "Company AJ", "Semiconductors", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The chip designer has been losing market share to a larger competitor, with its legacy products facing mounting pricing pressure and customer defections.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Analysts questioned the company's product roadmap, noting that its next-generation chip had been delayed multiple times and risked obsolescence upon arrival.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Short interest had risen to over 20% of the float, with bearish analysts predicting the company would run out of cash within 18 months if the new product failed.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company AJ stunned the market by announcing a breakthrough chip design that dramatically outperformed competitors in key AI benchmarks. Multiple hyperscaler customers placed immediate orders, and the stock surged 45%.","sentiment":"positive"},
], "AMD / Intel product launch comebacks — chip companies that reversed competitive losses with breakthrough product announcements.")

add_case("case_037", "Company AK", "Electric Vehicles", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The EV startup had been written off by most analysts after a series of production delays and quality issues that severely damaged its brand reputation.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Cash reserves were dwindling, and the company had reportedly hired restructuring advisors. Several key executives had departed in recent months.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"The stock was trading near all-time lows, and options markets were pricing in a high probability of bankruptcy within the next twelve months.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company AK shocked the industry by unveiling a mass-market EV with breakthrough battery technology at half the expected price point. Pre-orders flooded in, and a major automaker announced a strategic partnership. The stock rocketed 80% higher.","sentiment":"positive"},
], "Rivian R2/R3 launch / XPeng product announcements — EV companies revived by strong new product reception and strategic partnerships.")

add_case("case_038", "Company AL", "Artificial Intelligence", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The AI startup had generated enormous anticipation for its upcoming consumer hardware device, which was pitched as a revolutionary replacement for smartphones.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Celebrity endorsements and a viral marketing campaign drove unprecedented pre-launch interest. Industry analysts predicted the device would sell millions of units in its first year.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"The company's valuation had soared to billions of dollars ahead of the product launch, with venture capital firms competing to invest at ever-higher prices.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"The highly anticipated AI hardware device launched to scathing reviews, with critics citing poor battery life, frequent errors, and limited functionality. Return rates exceeded 90%, and the company was forced to slash prices. The stock collapsed 70%.","sentiment":"negative"},
], "Humane AI Pin / Rabbit R1 launch disaster — overhyped AI hardware products that failed catastrophically upon launch.")

add_case("case_039", "Company AM", "Pharmaceutical", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The pharma company's pipeline had been viewed as lackluster, with its lead drug candidate showing only marginal efficacy in mid-stage trials.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A competitor received approval for a drug targeting the same indication, which analysts said would capture the majority of the market before Company AM could reach the finish line.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Trading volume was light and the stock had drifted to multi-year lows, with most institutional investors having exited their positions.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company AM announced that the FDA had granted accelerated approval to its drug based on strong late-stage data that had been quietly compiled. Analysts upgraded the stock aggressively, calling the drug a potential blockbuster. Shares surged 120%.","sentiment":"positive"},
], "uniQure Huntington's drug accelerated approval / Precigen gene therapy approval — biotech stocks that skyrocketed on unexpected FDA greenlights.")

add_case("case_040", "Company AN", "Consumer Electronics", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The consumer electronics company had built significant buzz around its next-generation product, with tech reviewers and influencers hyping it as a potential category-defining device.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Pre-order numbers were reportedly strong, and the company had secured premium retail placement with major chains ahead of the launch date.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"The stock had rallied 50% in the six months leading up to the product launch, with analysts projecting the new device could double the company's revenue.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Shortly after the highly anticipated product launch, widespread reports of a critical safety defect emerged, and the company was forced to issue a global recall of 2.3 million units. The stock plunged 28% as analysts slashed estimates and questioned management credibility.","sentiment":"negative"},
], "Anker power bank recall / Samsung Galaxy Note battery recall — consumer electronics companies hit by massive post-launch safety recalls.")

# ============================================================
# Category 5: 管理层变动 (5 cases)
# ============================================================

add_case("case_041", "Company AO", "IT Services", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The IT services company has been executing well on its digital transformation strategy, with steady revenue growth and expanding margins under its long-tenured CEO.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A major client renewal was announced, extending a multi-year contract that analysts called a vote of confidence in Company AO's leadership and capabilities.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"The stock was trading near its 52-week high, with the upcoming earnings report widely expected to show continued steady performance.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Company AO shocked markets by announcing the immediate resignation of its CEO, alongside a sharp cut to revenue guidance. The board cited strategic differences, and the stock crashed 20% to a 52-week low as investors fled the uncertainty.","sentiment":"negative"},
], "Cyient CEO resignation + guidance cut / Salesforce co-CEO departure — companies where sudden CEO exits coincided with negative guidance revisions.")

add_case("case_042", "Company AP", "Automotive", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The legacy automaker had been praised for its ambitious electric vehicle transition plan, with the CEO receiving industry awards for bold leadership in a challenging transformation.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"New model launches had been well-received, and the company reported market share gains in key segments for the first time in several years.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Institutional investors had been accumulating the stock, which was viewed as undervalued relative to its EV transition progress and brand strength.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"The CEO abruptly resigned amid board disagreements over the pace of EV investment. The company also pre-announced a massive earnings miss, and the stock plunged 15% as the management vacuum raised existential questions about the turnaround strategy.","sentiment":"negative"},
], "Stellantis CEO Carlos Tavares resignation / Volkswagen CEO departure — automakers where CEO exits amid strategy disputes triggered sharp selloffs.")

add_case("case_043", "Company AQ", "Logistics", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The logistics and supply chain company had been posting steady results under its founder-CEO, with the stock outperforming its peer group over the past five years.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"An acquisition announced last year was integrating smoothly, and management highlighted cost synergies running ahead of plan at a recent investor event.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"The dividend was recently increased, signaling board confidence in the company's cash flow generation and growth trajectory.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Board turmoil erupted publicly as four independent directors resigned, citing irreconcilable differences with the founder-CEO over governance practices and related-party transactions. The stock plummeted 22% in a single session.","sentiment":"negative"},
], "WiseTech Global board resignations / multiple founder-CEO governance crises — companies where board mass resignations signaled deeper governance problems.")

add_case("case_044", "Company AR", "Gambling", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The sports betting and gaming company has been growing rapidly as more jurisdictions legalize online gambling, with revenue doubling year-over-year.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A successful expansion into a newly regulated market exceeded initial projections, and analysts raised their estimates for the company's addressable market.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Trading activity indicated strong institutional buying ahead of what was expected to be another record-breaking quarterly report.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"The CEO abruptly quit after only months in the role, catching the board and investors completely off guard. The company provided no clear explanation, and the stock tumbled 15% as uncertainty about strategy and leadership gripped the market.","sentiment":"negative"},
], "Entain CEO Gavin Isaacs departure after 161 days — gaming company CEOs quitting abruptly, creating leadership vacuum.")

add_case("case_045", "Company AS", "Consumer Staples", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The food and beverage conglomerate has been a defensive safe haven, consistently delivering mid-single-digit organic growth and steady margin expansion.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"The CEO's turnaround strategy had been widely credited with revitalizing the brand portfolio, and the company had just raised its dividend for the 25th consecutive year.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"A prominent analyst published a bullish deep-dive report arguing that Company AS was still in the early innings of a multi-year margin recovery story.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"The board abruptly ousted the CEO after less than two years, saying it wanted faster execution. The CFO was named as a replacement, but investors were rattled by the sudden change and lack of clear succession planning. The stock fell 7%.","sentiment":"negative"},
], "Unilever CEO Hein Schumacher ouster / Nestle CEO changes — consumer staples companies where abrupt CEO removals rattled investors.")

# ============================================================
# Category 6: 行业/宏观事件 (5 cases)
# ============================================================

add_case("case_046", "Company AT", "Oil & Gas", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"Crude oil prices had been rangebound between $70 and $80 per barrel, providing a stable and favorable environment for upstream producers like Company AT.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"OPEC+ maintained its production cuts, and geopolitical tensions in key producing regions added a risk premium to crude prices.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts expected Company AT to report strong free cash flow and announce an increased shareholder return program, given the supportive oil price environment.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"In a double shock, OPEC+ unexpectedly announced a significant production increase and new trade tariffs triggered a global growth scare. Crude oil prices crashed 16% in a single week, dragging Company AT's stock down 14%.","sentiment":"negative"},
], "April 2025 oil price crash — OPEC+ surprise production increase + Trump tariff shock causing oil to fall below $60/barrel.")

add_case("case_047", "Company AU", "Steel", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The steel producer was benefiting from strong domestic demand, with infrastructure spending and manufacturing activity supporting elevated steel prices.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Trade protections on imported steel were expected to remain in place, providing a durable competitive advantage for domestic producers like Company AU.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts recently upgraded the stock citing favorable supply-demand dynamics and the company's strong free cash flow generation at current steel prices.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Global trade tensions erupted as major economies imposed sweeping tariffs, triggering a broad selloff in industrial commodities. Steel prices tumbled, and Company AU's stock dropped 12% as recession fears mounted.","sentiment":"negative"},
], "2025 tariff war impact on steel/industrial stocks — trade tensions causing sharp corrections in commodity-exposed companies.")

add_case("case_048", "Company AV", "Airlines", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The airline industry faced severe headwinds as jet fuel prices spiked and consumer confidence surveys pointed to reduced travel intentions.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A major competitor warned that booking trends had deteriorated and announced capacity cuts, sending airline stocks sharply lower across the board.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts slashed earnings estimates for Company AV, predicting it would report a loss for the quarter and withdraw its full-year guidance.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Oil prices unexpectedly crashed after an OPEC+ production surprise, slashing Company AV's largest cost input. The airline raised its profit forecast dramatically, and shares surged 15%.","sentiment":"positive"},
], "Airlines benefiting from oil price crash — April 2025 oil price drop was a massive tailwind for fuel-heavy industries like aviation.")

add_case("case_049", "Company AW", "Gold Mining", "UP", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The gold miner had been underperforming as gold prices stagnated and production costs rose due to labor and energy inflation at its key mining operations.","sentiment":"negative"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"A production downgrade from a competitor highlighted the industry-wide challenges of declining ore grades and rising operational costs.","sentiment":"negative"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts predicted another quarter of margin compression, with gold prices failing to provide the tailwind needed to offset cost inflation.","sentiment":"negative"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Global financial markets plunged into turmoil as trade war fears intensified, triggering a massive flight to safety. Gold prices surged past all-time highs above $3,300 per ounce. Company AW's stock soared 22% as its profit outlook transformed overnight.","sentiment":"positive"},
], "Gold miners during April 2025 tariff shock — gold surged 22.5% to $3,350 as safe-haven demand exploded during the trade war panic.")

add_case("case_050", "Company AX", "Global Shipping", "DOWN", [
    {"id":"e1","time":"T-5","time_label":"5 days before prediction","text":"The container shipping company had been navigating Red Sea disruptions well, with rerouting around the Cape of Good Hope absorbing capacity and keeping freight rates elevated.","sentiment":"positive"},
    {"id":"e2","time":"T-3","time_label":"3 days before prediction","text":"Industry data showed global trade volumes holding up better than expected despite geopolitical uncertainties, with port throughput remaining near record levels.","sentiment":"positive"},
    {"id":"e3","time":"T-1","time_label":"1 day before prediction","text":"Analysts projected another strong quarter as supply chain disruptions effectively constrained shipping capacity, supporting freight rates well above pre-pandemic levels.","sentiment":"positive"},
], [
    {"id":"e4","time":"T+1","time_label":"1 day after prediction","text":"Global trade effectively seized up as a wave of punitive tariffs and retaliatory measures were announced. Shipping demand collapsed as companies canceled orders and suspended shipments, and Company AX's stock plunged 18% in a single day.","sentiment":"negative"},
], "Maersk / Hapag-Lloyd during tariff shock — shipping companies hit by sudden trade volume collapse from April 2025 tariff escalations.")

# ============================================================
# Write JSONL output
# ============================================================

output_path = "experiments/data/cases_draft_50.jsonl"
with open(output_path, "w", encoding="utf-8") as f:
    for case in cases:
        f.write(json.dumps(case, ensure_ascii=False) + "\n")

print(f"Wrote {len(cases)} cases to {output_path}")

# ============================================================
# Write sources document
# ============================================================

sources_path = "experiments/data/case_sources.md"
with open(sources_path, "w", encoding="utf-8") as f:
    f.write("# FinLeakAudit — 50 Case Sources\n\n")
    f.write("> 每个 case 背后的真实财经事件来源，用于审核时间线合理性和标注真实性。\n\n")
    f.write("---\n\n")

    categories = [
        ("财报超预期 Positive Surprise (label=UP)", range(0, 15)),
        ("财报低于预期 Negative Surprise (label=DOWN)", range(15, 30)),
        ("监管/诉讼冲击 (label=DOWN)", range(30, 35)),
        ("产品发布/重大合作 (Mixed)", range(35, 40)),
        ("管理层变动 (label=DOWN)", range(40, 45)),
        ("行业/宏观事件 (Mixed)", range(45, 50)),
    ]

    for cat_name, idx_range in categories:
        f.write(f"## {cat_name}\n\n")
        f.write("| Case ID | Company | Sector | Real Event Inspiration |\n")
        f.write("|---------|---------|--------|------------------------|\n")
        for i in idx_range:
            s = sources[i]
            f.write(f"| {s['case_id']} | {s['company']} | {s['sector']} | {s['real_event']} |\n")
        f.write("\n")

    # Summary statistics
    f.write("---\n\n")
    f.write("## 分布统计\n\n")
    f.write("| 类别 | 数量 | Label 分布 |\n")
    f.write("|------|------|------------|\n")
    f.write("| 财报超预期 | 15 | UP |\n")
    f.write("| 财报低于预期 | 15 | DOWN |\n")
    f.write("| 监管/诉讼冲击 | 5 | DOWN |\n")
    f.write("| 产品发布/重大合作 | 5 | 3 UP, 2 DOWN |\n")
    f.write("| 管理层变动 | 5 | DOWN |\n")
    f.write("| 行业/宏观事件 | 5 | 2 UP, 3 DOWN |\n")
    f.write("| **总计** | **50** | **20 UP, 30 DOWN** |\n\n")

    f.write("## 行业覆盖\n\n")
    f.write("半导体、消费零售、银行、医疗、能源、科技、航空航天、电商、制造业、媒体、电信、保险、酒店、农业、电动车、消费品、软件、医疗器械、云基础设施、奢侈品、网络安全、支付、房地产、广告、制药、游戏、家装、流媒体硬件、外卖、能源服务、硬件、金融科技、生物科技、加密货币、AI硬件、消费电子、IT服务、汽车、物流、博彩、消费品、油气、钢铁、航空、金矿、航运\n")

print(f"Wrote sources to {sources_path}")
print("Done!")
