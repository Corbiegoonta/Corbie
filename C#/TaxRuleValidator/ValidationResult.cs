


    public class ValidationResult
    {
        public int Id { get; set; }
        public int RuleId { get; set; }
        public int InvoiceId { get; set; }
        public bool Passed { get; set; }
        public DateTime ValidatedAt { get; set; } = DateTime.UtcNow;
    }
