

public class Invoice
{
    public int Id { get; set; }
    public decimal Amount { get; set; }
    public decimal VatRate { get; set; }
    public string Currency { get; set; } = null!;
    public string CustomerCountry { get; set; } = null!;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}