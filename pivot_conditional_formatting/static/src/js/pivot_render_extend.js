/** @odoo-module **/

    import { PivotRenderer } from "@web/views/pivot/pivot_renderer";
    import { PivotController } from "@web/views/pivot/pivot_controller";
    import { session } from "@web/session";
    import { useService } from "@web/core/utils/hooks";
    import { registry } from "@web/core/registry";
    import { patch } from '@web/core/utils/patch';
    const { useListener } = require("@web/core/utils/hooks");
    import { Record, RelationalModel } from "@web/views/basic_relational_model";
    const { useRef, Component, useExternalListener, onMounted, useEffect, useState , App, mount, onWillStart } = owl;

    patch(PivotRenderer.prototype,'pivot_render.patch',{
        setup() {
            this._super.apply();
            this.orm = useService("orm");

            this.mouse = 'test Mouse';
            this.isMouseDown = false;
            this.startRowIndex = null;
            this.startCellIndex = null;
            this.condition_array = []
            useExternalListener(document, 'mouseup', this.mouse_up_function)
            useEffect(() => {
                this.set_default_rules()
            })
        },

        async set_default_rules(){
            var self = this
            this.domain = ''
            var viewId = this.env.config.viewId
            var model = this.env.searchModel.resModel
            var search_id
            await this.orm.call("conditional.rules","search_read", [],{
                domain: [['model','=',model],['view_id','=',viewId]],
            }).then(function(res){
                self.conditional_rules = res
            })
            var cells = $('td')
            cells.each(function(data){
                cells[data].style.backgroundColor = "#f8f9fa"
                cells[data].style.color = "black"
            })
            $(".o_pivot.table-responsive table").find(".selected_cell").removeClass("selected_cell");
            $(".conditional_button").css({display:"none"})
            $(".conditional_container").css({display:"none"})

            for (let i = 0, len = this.conditional_rules.length; i < len; i++){
                var condition = this.conditional_rules[i].rule
                var condition_val = this.conditional_rules[i].value
                var second_condition_val = this.conditional_rules[i].second_value
                var color_val = this.conditional_rules[i].color
                var text_color_val = this.conditional_rules[i].text_color

                for (let j = 0, len = cells.length; j < len; j++){
                    var cell_val = cells[j].innerText
                    if(cell_val){
                        cell_val = cell_val.replace(',','')
                    }
                    if(condition == 'less_than'){
                        if(parseFloat(condition_val)>parseFloat(cell_val)){
                            cells[j].classList.remove("bg-100")
                            cells[j].style.backgroundColor = color_val
                            cells[j].style.color = text_color_val
                        }

                    }
                    if(condition == "greater_than"){
                        if(parseFloat(condition_val)< parseFloat(cell_val)){
                            cells[j].classList.remove("bg-100")
                            cells[j].style.backgroundColor = color_val
                            cells[j].style.color = text_color_val

                        }
                    }

                    if(condition == "is_empty"){
                        if(cells[j].innerText == ""){
                            cells[j].classList.remove("bg-100")
                            cells[j].style.backgroundColor = color_val
                            cells[j].style.color = text_color_val

                        }
                    }
                    if(condition == "in_between"){
                        if(parseFloat(cell_val)> parseFloat(condition_val) && parseFloat(cell_val)< parseFloat(second_condition_val)){
                            cells[j].classList.remove("bg-100")
                            cells[j].style.backgroundColor = color_val
                            cells[j].style.color = text_color_val
                        }
                    }
                }
            }
        },
        conditional_formattoo(e){
            if (e.target.localName == 'td' || e.target.className == 'o_value'){
                this.isMouseDown = true;
                var cell;
                if(e.target.className == 'o_value'){
                    cell = e.target.parentElement;
                }else{
                    cell = e.target
                }


                $(".o_pivot.table-responsive table").find(".selected_cell").removeClass("selected_cell"); // deselect everything

                    cell.className = 'selected_cell prevent-select'
                    this.startCellIndex = cell.cellIndex;
                    this.startRowIndex = cell.parentElement.cellIndex;


                return false; // prevent text selection
            }
        },


        mouse_over_function(e){
//            preventDefault(e)
            if (!this.isMouseDown) return;

            if (e.target.localName == 'td' || e.target.className == 'o_value'){
                var cell = e.target.parentElement;
                if(e.target.className == 'o_value'){
                    cell = e.target.parentElement;
                }else{
                    cell = e.target
                }
                cell.classList.add("selected_cell")
                $('.conditional_button').css({display:'block'})
            }
        },

        mouse_up_function(){
            this.isMouseDown = false;
        },

        display_field(){
            var condition = $('.condition_select option:selected').val()
            if(condition == 'in between'){
                $('#secondcondition_val').css({display:'block'})
                $('#value_label').css({display:'block'})
                $('#sub_input_container2').css({display:'flex'})
            }else{
                $('#secondcondition_val').css({display:'none'})
                $('#value_label').css({display:'none'})
                $('#sub_input_container2').css({display:'none'})
            }
        },
        set_rule(){
            var condition = $('.condition_select option:selected').val()
            var color_val = $('.colorpicker').val()
            var text_color_val = $('.text_color').val()
            var cells = $('.selected_cell')
            var condition_val = $('#condition_val').val()
            var second_condition_val = $('#secondcondition_val').val()
            if(condition_val< second_condition_val){
                return False
            }
            $('#condition_val')[0].value = ''
            $('#secondcondition_val')[0].value = ''
            for (let i = 0, len = cells.length; i < len; i++){
                var cell_val = cells[i].innerText
                if(cell_val){
                    cell_val = cell_val.replace(',','')
                }
                if(condition == 'less than'){
                    if(parseFloat(condition_val)>parseFloat(cell_val)){
                        cells[i].classList.remove("bg-100")
                        cells[i].style.backgroundColor = color_val
                        cells[i].style.color = text_color_val
                    }
                }
                if(condition == 'greater than'){
                    if(parseFloat(condition_val)< parseFloat(cell_val)){
                        cells[i].classList.remove("bg-100")
                        cells[i].style.backgroundColor = color_val
                        cells[i].style.color = text_color_val
                    }
                }
                if(condition == "null"){
                    if(cells[i].innerText == ""){
                        cells[i].classList.remove("bg-100")
                        cells[i].classList.remove("bg-100")
                        cells[i].style.backgroundColor = color_val
                        cells[i].style.color = text_color_val
                    }
                }
                if(condition == 'in between'){
                    if(parseFloat(cell_val)> parseFloat(condition_val) && parseFloat(cell_val)< parseFloat(second_condition_val)){
                        cells[i].classList.remove("bg-100")
                        cells[i].style.backgroundColor = color_val
                        cells[i].style.color = text_color_val
                    }
                }
            }
        },

    });
    patch(PivotController.prototype, 'PivotController.Patch', {
        setup() {
            this._super.apply();
        },
        conditional_format_tab(){
            console.log($('.selected_cell'))
        },

    });
