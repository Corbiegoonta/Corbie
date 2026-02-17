using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Mvc;
using Api.Data;



[ApiController]
[Route("api/[controller]")]
public class ValidationController : ControllerBase
{
    private readonly AppDbContext _db;
    private readonly IRuleEvaluator _evaluator;
    public ValidationController(AppDbContext db, IRuleEvaluator evaluator)
    {
        _evaluator = evaluator;
        _db = db;
    }
    [HttpPost]
    public async Task<IActionResult> Validate([FromBody] Invoice invoice)
    {
        var rules = await _db.Rules.ToListAsync();
        var results = new List<ValidationResult>();
        foreach (var rule in rules)
        {
            var passed = _evaluator.Evaluate(rule, invoice);
            results.Add(new ValidationResult
            {
                RuleId = rule.Id,
                InvoiceId = invoice.Id,
                Passed = passed,
                ValidatedAt = DateTime.UtcNow
            });
        }
        {
            _db.ValidationResults.AddRange(results);
            await _db.SaveChangesAsync();
        };
        return Ok(results);
    }
}