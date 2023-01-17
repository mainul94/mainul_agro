# Copyright (c) 2023, Mainul Islam and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(filters)


def get_data(filters):
	opening_date = filters.pop('from_date')
	closing_date = filters.pop('to_date')
	rows = []
	bank_and_cash_accounts = frappe.get_all('Account', {'account_type':('in', ('Bank', 'Cash')), 'is_group': 0}, pluck='name')
	# Opening
	opening = get_balance_on(bank_and_cash_accounts, opening_date, filters)
	rows.append(['<strong>'+_("Opening")+'</strong>', '', '', sum(x[2] for x in opening)])
	rows.extend(opening)
	# Transactions
	transactions = get_transactions(bank_and_cash_accounts, opening_date, closing_date, filters)
	receives = []
	payments = []
	r_total = 0
	p_total = 0
	for x in transactions:
		p, r = x[2], x[1]
		if r>0:
			r_total += r
			receives.append(['', x[0], r,''])
		if p>0:
			p_total += p
			payments.append(['', x[0], p, ''])
	rows.append(['<strong>'+_("Transaction") + "(Receipt - Payment)"+'</strong>', '', '', r_total-p_total])
	rows.append(['', '<strong>'+_("Receipt") +'</strong>', '', r_total])
	rows.extend(receives)
	rows.append(['', '<strong>'+_("Payment") +'</strong>', '', p_total])
	rows.extend(payments)
	# Closing
	closing = get_balance_on(bank_and_cash_accounts, closing_date, filters, False)
	rows.append(['<strong>'+_("Closing")+'</strong>', '', '', sum(x[2] for x in closing)])
	rows.extend(closing)
	return rows


def get_transactions(accounts, opening_date, closing_date, filters):
	cond = ["is_cancelled=0", 'company="{}"'.format(filters.get('company')),
		'posting_date >= date("{}")'.format(opening_date), 'posting_date <= date("{}")'.format(closing_date)]
	for key in ('project', 'branch'):
		if filters.get(key):
			cond.append('project="{}"'.format(filters[key]))
	cond.append('against in ("{}")'.format('", "'.join(accounts)))
	return frappe.db.sql("""select account, sum(credit), sum(debit) from `tabGL Entry` where {} group by account""".format(" and ".join(cond)))


def get_balance_on(accounts, date, filters, opening=True):
	cond = ["is_cancelled=0", 'company="{}"'.format(filters.get('company')),
		'posting_date {} date("{}")'.format('<' if opening else'<=', date)]
	for key in ('project', 'branch'):
		if filters.get(key):
			cond.append('project="{}"'.format(filters[key]))
	cond.append('account in ("{}")'.format('", "'.join(accounts)))
	return frappe.db.sql("""select ""as label, account, sum(debit)-sum(credit), ""as sub_total from `tabGL Entry` where {} group by account""".format(" and ".join(cond)))

def get_columns():
	return [
		_("Label") + ":Data:200",
		_("Account") + ":Link/Account:200",
		_("Balance/Amount") + ":Currency:100",
		_("Sub Total") + ":Currency:100"
	]
