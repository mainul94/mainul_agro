// Copyright (c) 2023, Mainul Islam and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Receipt and Payment Statement"] = {
	"filters": [
		{
			fieldname: 'company',
			fieldtype: 'Link',
			options: 'Company',
			reqd: 1,
			default: frappe.defaults.get_user_default('company')
		},
		{
			fieldname: 'from_date',
			fieldtype: 'Date',
			reqd: 1,
			default: frappe.datetime.get_today()
		},
		{
			fieldname: 'to_date',
			fieldtype: 'Date',
			reqd: 1,
			default: frappe.datetime.get_today()
		},
		{
			fieldname: 'project',
			fieldtype: 'Link',
			options: 'Project'
		},
		{
			fieldname: 'branch',
			fieldtype: 'Link',
			options: 'Branch'
		}		
	]
};
