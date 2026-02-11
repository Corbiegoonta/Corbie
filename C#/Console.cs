using Newtonsoft.Json.Linq;
using Spectre.Console;
using MarketMaster;


static void GUIConsole(Task<string> jsonData)
    {
      var table = new Table();
        table.AddColumn("From Currency");
        table.AddColumn("To Currency");
        table.AddColumn("Exchange Rate");
     JObject jd = JObject.Parse(jsonData.Result);
    Console.WriteLine("Parsed JSON data: " + jd);
            string fromCurrency = jd["Realtime Currency Exchange Rate"]["1. From_Currency Code"].ToString();
            string toCurrency = jd["Realtime Currency Exchange Rate"]["3. To_Currency Code"].ToString();
            string exchangeRate = jd["Realtime Currency Exchange Rate"]["5. Exchange Rate"].ToString();
            table.AddRow(fromCurrency, toCurrency, exchangeRate);
    AnsiConsole.Write(table);
    
}
AnsiConsole.MarkupLine("[green]✓ Build completed successfully[/]");
dynamic tab = Programs.GetPriceAsync("GBP", "USD", "");
GUIConsole(tab);