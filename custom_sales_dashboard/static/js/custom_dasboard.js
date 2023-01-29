odoo.define('custom_sales_dashboard.custom_dashboard', function (require){
"use strict";
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var QWeb = core.qweb;
var rpc = require('web.rpc');
var ajax = require('web.ajax');
const { loadBundle }  = require("@web/core/assets");


var CustomSalesDashBoard = AbstractAction.extend({
   template: 'SalesCustomDashBoard',
   events: {
        'click .team-name': 'team_details',
        'click .person-name': 'person_details',
        'click #go_back': 'team_display',
        'click #go_back2': 'person_display',
        'click .all_team_orders': 'all_team_orders',
        'click .all_person_orders': 'all_sale_orders',
        'click .customer-name': 'all_customer_orders',
        'click .sale_state': 'sale_state_orders',
        'click .invoice_state': 'invoice_state_orders',
   },

   init: function(parent, context) {
       this._super(parent, context);
       this.dashboards_templates = ['SalesCustomDashBoardBody'];
   },
   willStart: function() {
       var self = this;
       return $.when(loadBundle(this), this._super()).then(function() {
           return self.fetch_data();
       });
   },

   start: function(){
        var self = this;
           this.set("title", 'Dashboard');
           return this._super().then(function() {
               self.render_dashboards();
               self.bar_chart();
           });
       },
   render_dashboards: function(){
       var self = this;
       _.each(this.dashboards_templates, function(template) {
               self.$el.append(QWeb.render(template, {widget: self}));
           });

   },

   fetch_data: function() {
       var self = this;
       var def1 =  this._rpc({
               route: '/sales_dashboard',
       }).then(function(res)
        {
            self.record = res.record
            self.sales_person = res.sales_person
            self.customers = res.customers
            self.product_count = res.product_count
            self.sale_states = res.sale_states
            self.invoice_states = res.invoice_states

       });
           return $.when(def1);
   },
   team_details: function(ev){
        var self = this;

        var id = ev.currentTarget.dataset['id']
        this._rpc({
               model: 'crm.team',
               method: 'search_read',
               args: [[['id', '=', parseInt(id)]]]
       }).then(function(res)
        {
           $('#team-heading').text(res[0].name)
           $('#quotations').text("Quotations: "+res[0].quotations_count)
           $('#sale_ord').text("Sale Orders: "+res[0].sale_order_count)
           $('#ord_inv').text("Orders To Invoice: "+res[0].sales_to_invoice_count)
           $('#inv_amt').text("Invoiced: "+res[0].invoiced+" / "+res[0].invoiced_target)
           document.querySelector('.all_team_orders').setAttribute("id",res[0].id );
       });

       $("#team-tab2").toggle()
       $("#team-tab").toggle()
   },
   team_display: function(){
        $("#team-tab2").toggle()
        $("#team-tab").toggle()
   },
   person_details: function(ev){
        var self = this;
        $("#person-tab1").toggle()
        $("#person-tab2").toggle()
        var id = ev.currentTarget.dataset['id']
        this._rpc({
               route: '/sales_dashboard',
       }).then(function(res)
        {
            var record = res.sales_person
            for (let i = 0, len = record.length; i < len; i++) {
                if(id == record[i].id){
                    $('#person-heading').text(record[i].name)
                    $('#sale_count').text("Sale Orders: "+record[i].order_count)
                    $('#total_amt').text("Total Amount: "+record[i].total_amt)
                    document.querySelector('.all_person_orders').setAttribute("id",record[i].id );
                }

            }
       });
   },
   person_display: function(){
        $("#person-tab1").toggle()
        $("#person-tab2").toggle()
   },
   all_team_orders: function(ev){
        var id = ev.currentTarget.id
        this.do_action({
             name: "Team Orders",
             type: 'ir.actions.act_window',
             res_model: 'sale.order',
             view_mode: 'tree,form,calendar',
             views: [[false, 'list'],[false, 'form']],
             domain: [['team_id', '=', parseInt(id)]],
             target: 'current',
         })
   },
   all_sale_orders: function(ev){
        var id = ev.currentTarget.id
        this.do_action({
             name: "SalesPerson Orders",
             type: 'ir.actions.act_window',
             res_model: 'sale.order',
             view_mode: 'tree,form,calendar',
             views: [[false, 'list'],[false, 'form']],
             domain: [['user_id', '=', parseInt(id)]],
             target: 'current',
         })
   },
   all_customer_orders: function(ev){
        var id = ev.currentTarget.dataset['id']
        this.do_action({
             name: "Customer Orders",
             type: 'ir.actions.act_window',
             res_model: 'sale.order',
             view_mode: 'tree,form,calendar',
             views: [[false, 'list'],[false, 'form']],
             domain: [['partner_id', '=', parseInt(id)]],
             target: 'current',
         })
   },
   bar_chart: function(){
        this._rpc({
               route: '/sales_dashboard',
       }).then(function(res)
        {
            var lowest_selling = res.lowest_selling

            var highest_selling = res.highest_selling
            var xValues = [highest_selling[0]['name'], highest_selling[1]['name'],
                highest_selling[2]['name'], highest_selling[3]['name'],
                highest_selling[4]['name'], highest_selling[5]['name'],
                highest_selling[6]['name']];

            var yValues = [highest_selling[0]['count'], highest_selling[1]['count'],
                highest_selling[2]['count'], highest_selling[3]['count'],
                highest_selling[4]['count'], highest_selling[5]['count'],
                highest_selling[6]['count']];
            var barColors = ["#8572c1", "#8572c1","#8572c1",
                "#8572c1","#8572c1","#8572c1","#8572c1"];

            var ctx = $('#myChart')

            new Chart(ctx, {
              type: "bar",
              data: {
                labels: xValues,
                datasets: [{
                  backgroundColor: barColors,
                  data: yValues
                }]
              },
              options: {
                legend: {display: false},
                title: {
                  display: true,
                  text: "Highest Selling Product"
                }
              }
            });


            var x2Values = [lowest_selling[0]['name'], lowest_selling[1]['name'],
                lowest_selling[2]['name'], lowest_selling[3]['name'],
                lowest_selling[4]['name'], lowest_selling[5]['name'],
                lowest_selling[6]['name']];

            var y2Values = [lowest_selling[0]['count'], lowest_selling[1]['count'],
                lowest_selling[2]['count'], lowest_selling[3]['count'],
                lowest_selling[4]['count'], lowest_selling[5]['count'],
                lowest_selling[6]['count']];
            var barColors = ["#8572c1", "#8572c1","#8572c1",
                "#8572c1","#8572c1","#8572c1","#8572c1"];

            var ctx2 = $('#myChart2')

            new Chart(ctx2, {
              type: "bar",
              data: {
                labels: x2Values,
                datasets: [{
                  backgroundColor: barColors,
                  data: y2Values
                }]
              },
              options: {
                legend: {display: false},
                title: {
                  display: true,
                  text: "Lowest Selling Product"
                }
              }
            });
        })

   },

   sale_state_orders: function(ev){
        var state = ev.currentTarget.id
        this.do_action({
             name: "Sale Orders",
             type: 'ir.actions.act_window',
             res_model: 'sale.order',
             view_mode: 'tree,form,calendar',
             views: [[false, 'list'],[false, 'form']],
             domain: [['state', '=', state]],
             target: 'current',
         })
   },

   invoice_state_orders: function(ev){
        var state = ev.currentTarget.id
        this.do_action({
             name: "Sale Orders",
             type: 'ir.actions.act_window',
             res_model: 'sale.order',
             view_mode: 'tree,form,calendar',
             views: [[false, 'list'],[false, 'form']],
             domain: [['invoice_status', '=', state]],
             target: 'current',
         })
   },


})
core.action_registry.add('sales_custom_dashboard', CustomSalesDashBoard);
return CustomSalesDashBoard;
})