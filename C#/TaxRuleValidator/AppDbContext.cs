using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;
using System.Formats.Asn1;


namespace Api.Data
{

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<Rule> Rules { get; set; }
        public DbSet<Invoice> Invoices { get; set; }
        public DbSet<ValidationResult> ValidationResults { get; set; }
    }
}