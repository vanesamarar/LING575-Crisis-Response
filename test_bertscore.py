from bert_score import score as bert_score
bts = ["This is a back-translated alert message."]
refs = ["This is the original English alert message."]
P, R, F1 = bert_score(bts, refs, lang="en", rescale_with_baseline=True)
print(F1)  # Should be positive and reasonable

