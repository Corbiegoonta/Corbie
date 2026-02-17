//using NCalc;

public interface IRuleEvaluator { bool Evaluate(Rule rule, Invoice invoice); }

public class RuleEvaluator : IRuleEvaluator
{
    public bool Evaluate(Rule rule, Invoice invoice)
    {
    var expr = new NCalc.Expression(rule.Expression);
    expr.Parameters["amount"] = invoice.Amount;
    expr.Parameters["vatRate"] = invoice.VatRate;
    return (bool)expr.Evaluate();
    }
}