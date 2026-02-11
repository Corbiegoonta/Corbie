namespace MarketMaster
{
    class Programs
    {
        static readonly HttpClient client = new HttpClient();

        public static async Task<string> GetPriceAsync(string fromCurrency, string toCurrency, string api_key)
        {
            Console.WriteLine($"Fetching conversion currency exchange rate from {fromCurrency} to {toCurrency}");
            var response = await client.GetAsync($"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={fromCurrency}&to_currency={toCurrency}&apikey={api_key}");
            response.EnsureSuccessStatusCode();
            Console.WriteLine("API call successful. Processing response...");
            string responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine("Response body: " + responseBody);

            return responseBody;

            throw new NotImplementedException();
        }

        static void Main(string[] args)
        {
    //        var assets = new List<MarketMaster.Asset>
    //{
    //    new MarketMaster.Asset
    //    {
    //        Ticker = "AAPL",
    //        Shares = 10,
    //        CostBasis = 1500,
    //        Type = "Stock",
    //        Price = "170",
    //        PurchaseDate = new DateTime(2020, 1, 1),
    //        Sector = "Technology"
    //    },
    //    new MarketMaster.Asset
    //    {
    //        Ticker = "GOOGL",
    //        Shares = 5,
    //        CostBasis = 5000,
    //        Type = "Stock",
    //        Price = "2800",
    //        PurchaseDate = new DateTime(2021, 6, 15),
    //        Sector = "Technology"
    //    }
    //};

    //        for (int i = 0; i < assets.Count(); i++)
    //            Console.WriteLine(assets[i].Ticker);
    //        foreach (var asset in assets)
    //            Console.WriteLine(asset.Ticker);
    //        //PortfolioUtil.PrintPortfolio(assets);
    //        PortfolioUtil.SavePortfolio(assets, "C:\\Users\\nickc\\Desktop\\portfolio.json");
    //        Console.WriteLine("Portfolio has been saved to C:\\Users\\nickc\\Desktop\\portfolio.json");
            //string ticker = "GOOG";
            //string url = $"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey=";
            //string jsonResponse = await response.Content.;
            //Uri uri = new Uri(url);
            //using HttpResponseMessage response = client.GetAsync(uri).Result;
            //Console.WriteLine(response);
            //dynamic json_data = JsonSerializer.Deserialize<HttpRequestMessage>(response);
            try
            {
                dynamic json = GetPriceAsync("GBP", "USD", "WHGFYQHHC4FSCJ39").Result;
                Console.WriteLine("Output: " + json);
                string fromCurrency = json["Realtime Currency Exchange Rate"]["1. From_Currency Code"];
                string toCurrency = json["Realtime Currency Exchange Rate"]["3. To_Currency Code"];
                string curencyName = json["Realtime Currency Exchange Rate"]["2. From_Currency Name"];
                string toCurrencyName = json["Realtime Currency Exchange Rate"]["4. To_Currency Name"];
                decimal exchangeRate = Convert.ToDecimal(json["Realtime Currency Exchange Rate"]["5. Exchange Rate"]);
                DateTime lastRefreshed = Convert.ToDateTime(json["Realtime Currency Exchange Rate"]["6. Last Refreshed"]);
                string timeZone = json["Realtime Currency Exchange Rate"]["7. Time Zone"];
                string bidPrice = json["Realtime Currency Exchange Rate"]["8. Bid Price"];
                string askPrice = json["Realtime Currency Exchange Rate"]["9. Ask Price"];
                Console.WriteLine("From Currency: " + fromCurrency);
                Console.WriteLine("To Currency: " + toCurrency);
                Console.WriteLine("Currency Name: " + curencyName);
                Console.WriteLine("To Currency Name: " + toCurrencyName);
                Console.WriteLine("Exchange Rate: " + exchangeRate);
                Console.WriteLine("Last Refreshed: " + lastRefreshed);
                Console.WriteLine("Time Zone: " + timeZone);
                Console.WriteLine("Bid Price: " + bidPrice);
                Console.WriteLine("Ask Price: " + askPrice);

            }

            catch (Exception ex)
            {
                Console.WriteLine("Error fetching price: " + ex.Message);
            }
        }

    }
}


