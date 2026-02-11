using System;
using System.Collections.Generic;
using System.Text;

namespace MarketMaster
{
    using System;
    using System.Text.Json.Serialization;

    public class AlphaVantageResponse
    {
        [JsonPropertyName("Global Quote")]
        public Asset Asset { get; set; }
    }

    public class Asset
    {
        public string? Ticker { get; set; }
        public decimal Shares { get; set; }
        public decimal CostBasis { get; set; } // Cost basis is the total original value of an asset—purchase price plus fees, commissions, and adjustments (like dividends or1099-B, stock splits)—used to determine capital gains or losses for tax purposes when sold. It is critical for calculating taxable profit, typically calculated as the sale price minus the adjusted cost basis. 
        public string? Type { get; set; }
        public string? Price { get; set; }
        //public decimal CurrentValue => Shares * (decimal)Price;
        //public decimal GainLoss => CurrentValue - CostBasis;
        //public decimal GainLossPercentage => CostBasis != 0 ? Math.Round((GainLoss / CostBasis) * 100, 3) : 0;
        public DateTime PurchaseDate { get; set; }
        public DateTime? SaleDate { get; set; }
        public string? Sector { get; set; }
    }
}
