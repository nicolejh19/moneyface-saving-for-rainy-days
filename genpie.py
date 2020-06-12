import pygal

chat_id = "ID USED FOR TESTING"
curr_food_exp = dbhelper.get_monthly_category_exp(chat_id, year_month, 'FOOD')
curr_clothes_exp = dbhelper.get_monthly_category_exp(chat_id, year_month, 'CLOTHES')
curr_transport_exp = dbhelper.get_monthly_category_exp(chat_id, year_month, 'TRANSPORT')
curr_necc_exp = dbhelper.get_monthly_category_exp(chat_id, year_month, 'NECESSITIES')
curr_others_exp = dbhelper.get_monthly_category_exp(chat_id, year_month, 'OTHERS')
pie_chart = pygal.Pie()
pie_chart.title = 'Current monthly expenditure (in %)'
results = [(convert_str(curr_food_exp),'FOOD'), (convert_str(curr_clothes_exp),'CLOTHES'), (convert_str(curr_transport_exp),'TRANSPORT'), (convert_str(curr_necc_exp),'NECESSITIES'), (convert_str(curr_others_exp),'OTHERS')]
for r in results:
    pie_chart.add(r[1], [{'value': r[0], 'label': r[1]}])
    pie_chart.render_tree() 
