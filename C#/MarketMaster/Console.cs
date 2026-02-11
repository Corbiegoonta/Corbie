using Newtonsoft.Json.Linq;
using Spectre.Console;
using MarketMaster;


static void GUIConsole(Task<string> jsonData)
    {
      var table = new Table();
        table.AddColumn("From Currency");
        table.AddColumn("From Currency Name");
        table.AddColumn("To Currency");
        table.AddColumn("To Currency Name");
        table.AddColumn("Exchange Rate");
        table.AddColumn("Last Refreshed");
        table.AddColumn("Time Zone");
        table.AddColumn("Bid Price");
        table.AddColumn("Ask Price");
    JObject jd = JObject.Parse(jsonData.Result);
    Console.WriteLine("Parsed JSON data: " + jd);
            string fromCurrency = jd["Realtime Currency Exchange Rate"]["1. From_Currency Code"].ToString();
            string fromCurrencyName = jd["Realtime Currency Exchange Rate"]["2. From_Currency Name"].ToString();
            string toCurrency = jd["Realtime Currency Exchange Rate"]["3. To_Currency Code"].ToString();
            string toCurrencyName = jd["Realtime Currency Exchange Rate"]["4. To_Currency Name"].ToString();
            string exchangeRate = jd["Realtime Currency Exchange Rate"]["5. Exchange Rate"].ToString();
            string lastRefreshed = jd["Realtime Currency Exchange Rate"]["6. Last Refreshed"].ToString();
            string timeZone = jd["Realtime Currency Exchange Rate"]["7. Time Zone"].ToString();
            string bidPrice = jd["Realtime Currency Exchange Rate"]["8. Bid Price"].ToString();
            string askPrice = jd["Realtime Currency Exchange Rate"]["9. Ask Price"].ToString();

    table.AddRow(fromCurrency, fromCurrencyName, toCurrency, toCurrencyName, exchangeRate, lastRefreshed, timeZone, bidPrice, askPrice);
    AnsiConsole.Write(table);
    
}
AnsiConsole.MarkupLine("[green]✓ Build completed successfully[/]");
dynamic tab = Programs.GetPriceAsync("GBP", "USD", "WHGFYQHHC4FSCJ39");
GUIConsole(tab);

