import pandas as pd

def check_forbidden_word(output, forbidden_word):
    """Returns True if the constraint was violated (word found)."""
    return forbidden_word.lower() in output.lower()

def check_format(output, required_format):
    """Returns True if the format constraint was met."""
    if required_format == 'numbered_list':
        return "1." in output and "2." in output
    elif required_format == 'bullet_points':
        return "-" in output or "*" in output
    elif required_format == 'paragraphs':
        return "\n\n" in output
    return False

# Load dataset
df = pd.read_csv('constraint_dataset.csv')

# Run automated evaluation
print("Running automated constraint evaluation...\n")
df['failed_negative_constraint'] = df.apply(lambda row: check_forbidden_word(row['mock_model_output'], row['forbidden_word']), axis=1)
df['met_format_constraint'] = df.apply(lambda row: check_format(row['mock_model_output'], row['required_format']), axis=1)

# Determine final pass/fail
df['overall_pass'] = (~df['failed_negative_constraint']) & (df['met_format_constraint'])

# Display Results
for index, row in df.iterrows():
    status = "PASS" if row['overall_pass'] else "FAIL"
    print(f"Prompt {row['prompt_id']} [{status}]:")
    print(f"  - Avoided '{row['forbidden_word']}': {not row['failed_negative_constraint']}")
    print(f"  - Followed '{row['required_format']}': {row['met_format_constraint']}\n")

# Summary metrics
pass_rate = (df['overall_pass'].sum() / len(df)) * 100
print(f"Overall Constraint Adherence Rate: {pass_rate}%")
