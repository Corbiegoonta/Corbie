

public class Rule
{
    public int Id { get; set; }
    public string Jurisdiction { get; set; } = null!;
    public string Expression { get; set; } = null!;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
   