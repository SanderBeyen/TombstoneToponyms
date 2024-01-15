def parse_identifiers(line):
    """Parse identifiers from a formatted line"""
    parts = line.split()
    if len(parts) > 1:
        filename = parts[0]
        identifiers = parts[1:]
        return filename, identifiers
    return None, None


def compare_results(system_file, gold_standard_file):
    """Compare system results and gold standard based """
    system_data = {}
    gold_standard_data = {}
    overall_system_identifiers = set()
    overall_gold_standard_identifiers = set()
    overall_true_positives = 0
    evaluation_metrics = {}  # Individual evaluation metrics for each file

    # Read system results
    with open("Found_Toponyms.txt", 'r') as system_file:
        for line in system_file:
            filename, identifiers = parse_identifiers(line.strip())
            if filename and identifiers:
                system_data[filename] = set(identifiers)  # Using set to ignore order
                overall_system_identifiers.update(identifiers)

    # Read gold standard
    with open("gold_standard.txt", 'r') as gold_standard_file:
        for line in gold_standard_file:
            filename, identifiers = parse_identifiers(line.strip())
            if filename and identifiers:
                gold_standard_data[filename] = set(identifiers)  # Using set to ignore order
                overall_gold_standard_identifiers.update(identifiers)

    # Compare results and calculate individual evaluation metrics
    for filename, system_identifiers in system_data.items():
        if filename in gold_standard_data:
            gold_standard_identifiers = gold_standard_data[filename]
            true_positives = len(system_identifiers.intersection(gold_standard_identifiers))
            precision, recall, f1_score = evaluate_results(system_identifiers, gold_standard_identifiers, true_positives)
            evaluation_metrics[filename] = {'Precision': precision, 'Recall': recall, 'F1-Score': f1_score}
            overall_true_positives += true_positives

    # Calculate overall evaluation metrics
    overall_precision, overall_recall, overall_f1_score = evaluate_results(
        overall_system_identifiers, overall_gold_standard_identifiers, overall_true_positives
    )

    evaluation_metrics['Overall'] = {'Precision': overall_precision, 'Recall': overall_recall, 'F1-Score': overall_f1_score}

    return evaluation_metrics


def evaluate_results(system_results, gold_standard, true_positives):
    """Calculate precision, recall, and F1-score """
    precision = true_positives / len(system_results) if len(system_results) > 0 else 0
    recall = true_positives / len(gold_standard) if len(gold_standard) > 0 else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1_score


# Compare results
evaluation_results = compare_results('Found_Toponyms.txt', 'gold_standard.txt')

# Print individual evaluation metrics for each file and overall metrics
for filename, metrics in evaluation_results.items():
    print(f"Filename: {filename}")
    print(f"Precision: {metrics['Precision']:.2f}")
    print(f"Recall: {metrics['Recall']:.2f}")
    print(f"F1-Score: {metrics['F1-Score']:.2f}")
    print("------------")
