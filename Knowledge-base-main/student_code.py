class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True



class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        if match(fact.statement, rule.lhs[0], None):
            bind_new = match(fact.statement, rule.lhs[0], None)
            rhs_new = instantiate(rule.rhs, bind_new)
            lhs_new = rule.lhs[1:]

            if len(lhs_new) == 0:
                fact_new = Fact(rhs_new, [[fact, rule]])
                kb.kb_assert(fact_new)
                fact.supports_facts.append(fact_new)
                rule.supports_rules.append(fact_new)
            else:
                for i in range(len(lhs_new)):
                    lhs_new[i] = instantiate(lhs_new[i], bind_new)

                rule_new = Rule([lhs_new, rhs_new], [[fact, rule]])
                kb.kb_assert(rule_new)
                fact.supports_rules.append(rule_new)
                rule.supports_rules.append(rule_new)
