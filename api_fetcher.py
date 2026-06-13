import aiohttp
import asyncio

async def get_market_data():
    FIAT_URL = "https://raw.githubusercontent.com/meytiii/sarraf-bashi-bot/main/data/fiat.json"
    GOLD_URL = "https://raw.githubusercontent.com/meytiii/sarraf-bashi-bot/main/data/gold.json"
    
    results = {
        "usd": "نامشخص",
        "eur": "نامشخص",
        "gold_18k": "نامشخص",
        "silver_ounce": "نامشخص"
    }

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        try:
            async with session.get(FIAT_URL) as response:
                if response.status == 200:
                    fiat_data = await response.json()
                    
                    if "usd" in fiat_data:
                        results["usd"] = f"{int(fiat_data['usd']['value']):,} تومان"
                    if "eur" in fiat_data:
                        results["eur"] = f"{int(fiat_data['eur']['value']):,} تومان"
            
            async with session.get(GOLD_URL) as response:
                if response.status == 200:
                    gold_data = await response.json()
                    
                    if "18ayar" in gold_data:
                        results["gold_18k"] = f"{int(gold_data['18ayar']['value']):,} تومان"
            
            async with session.get(FIAT_URL) as response:
                if response.status == 200:
                    fiat_data = await response.json()
                    if "xag" in fiat_data:
                        results["silver_ounce"] = f"{int(fiat_data['xag']['value']):,} دلار"

            return results

        except Exception as e:
            print(f"🚨 GitHub Fetch Error: {e}")
            return None

if __name__ == "__main__":
    async def test_api():
        print("Testing GitHub Raw JSON fetch...")
        data = await get_market_data()
        print("\n--- FINAL RESULT ---")
        print(data)
        
    asyncio.run(test_api())