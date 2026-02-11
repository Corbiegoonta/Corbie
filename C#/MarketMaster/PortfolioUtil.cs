using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Security.Cryptography.X509Certificates;
using System.Text.Json;

namespace MarketMaster
{
    public static class PortfolioUtil
    {
        public static void AddAsset(List<Asset> portfolio, Asset asset)
        {
            portfolio.Add(asset);
        }

        public static void RemoveAsset(List<Asset> portfolio, string ticker)
        {
            var assetToRemove = portfolio.Find(a => a.Ticker == ticker);
            if (assetToRemove != null)
            {
                portfolio.Remove(assetToRemove);
            }
        }

        //public static decimal CalculateTotalValue(List<Asset> portfolio)
        //{
        //    IEnumerable<decimal> assetValues = portfolio.Select(a => a.CurrentValue);
        //    decimal totalValue = 0;
        //    foreach (var asset in assetValues)
        //    {
        //        totalValue += asset;
        //    }
        //    return totalValue;
        //}
        //public static decimal CalculateTotalGainLoss(List<Asset> portfolio)
        //{
        //    IEnumerable<decimal> assetGainsLosses = portfolio.Select(a => a.GainLoss);
        //    decimal totalGainLoss = 0;
        //    foreach (var asset in assetGainsLosses)
        //    {
        //        totalGainLoss += asset;
        //    }
        //    return totalGainLoss;
        //}
        
        //public static decimal CalculateTotalGainLossPercentage(List<Asset> portfolio)
        //{
        //    decimal totalCostBasis = portfolio.Sum(a => a.CostBasis);
        //    decimal totalGainLoss = CalculateTotalGainLoss(portfolio);
        //    return totalCostBasis != 0 ? (totalGainLoss / totalCostBasis) * 100 : 0;
        //}

        //public static void PrintPortfolio(List<Asset> portfolio)
        //{
        //    Console.WriteLine("Ticker\tShares\tCost Basis\tCurrent Price\tCurrent Value\tGain/Loss\tGain/Loss %\tPurchase Date\tSector");
        //    foreach (var asset in portfolio)
        //    {
        //        Console.WriteLine($"{asset.Ticker}\t{asset.Shares}\t{asset.CostBasis:C}\t{asset.CurrentPrice:C}\t{asset.CurrentValue:C}\t{asset.GainLoss:C}\t{asset.GainLossPercentage:F2}%\t{asset.PurchaseDate:d}\t{asset.Sector}");
        //    }
        //}

        public static void SavePortfolio(List<Asset> portfolio, string saveLocation)
        {
            var output = JsonSerializer.Serialize(portfolio);
            File.WriteAllText(saveLocation, output);
        }

        public static List<Asset> LoadPortfolio(string fileLocation)
        {
            if (!File.Exists(fileLocation))
            {
                Console.WriteLine($"File not found at: {fileLocation}. A new asset list has been returned");
                return new List<Asset>();
            }
            try
            {
                var json = File.ReadAllText(fileLocation);
                var portfolio = JsonSerializer.Deserialize<List<Asset>>(json);
                if (portfolio != null)
                    Console.WriteLine($"Portfolio was loaded successfully and returned from: {fileLocation}");
                else                    
                    Console.WriteLine($"Portfolio was loaded successfully but returned null from: {fileLocation}. A new asset list has been returned");
                    return new List<Asset>();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error loading portfolio: {ex.Message}");
                Console.WriteLine("A new asset list has been returned");
                return new List<Asset>();
            }
        }
    }
}
