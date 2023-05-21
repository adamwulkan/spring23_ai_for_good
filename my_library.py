def compute_probs(neg,pos):
  p0 = neg/(neg+pos)
  p1 = pos/(neg+pos)
  return [p0,p1]

def test_it():
  return 'loaded'

def cond_prob(table, evidence, evidence_value, target, target_value):
  t_subset = up_table_subset(table, target, 'equals', target_value)
  e_list = up_get_column(t_subset, evidence)
  p_b_a = sum([1 if v==evidence_value else 0 for v in e_list])/len(e_list)
  return p_b_a + .01

def cond_probs_product(your_table, your_evidence_values, your_target_column, your_target_value):
  your_table_columns = up_list_column_names(your_table)
  your_evidence_columns = your_table_columns[:-1]
  your_evidence_complete = up_zip_lists(your_evidence_columns, your_evidence_values)
  cond_prob_list = []
  for item in your_evidence_complete:
    all_probs = cond_prob(your_table, item[0], item[1], your_target_column, your_target_value)
    cond_prob_list += [all_probs]
  return up_product(cond_prob_list)

def prior_prob(your_table, your_target, your_target_value):
  t_list = up_get_column(your_table, your_target)
  p_a = sum([1 if v==your_target_value else 0 for v in t_list])/len(t_list)
  return p_a

def naive_bayes(table, evidence_row, target):
  #compute P(Flu=0|...) by collecting cond_probs in a list, take the produce of the list, finally multiply by P(Flu=0)
  neg_cond_prob = cond_probs_product(table, evidence_row, target, 0) * prior_prob(table, target, 0)

  #do same for P(Flu=1|...)
  pos_cond_prob = cond_probs_product(table, evidence_row, target, 1) * prior_prob(table, target, 1)

  #Use compute_probs to get 2 probabilities
  neg, pos = compute_probs(neg_cond_prob, pos_cond_prob)
  
  #return your 2 results in a list
  return [neg, pos]
