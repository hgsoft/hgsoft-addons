/* /shop_batch_sales/static/src/js/scripts2.js defined in bundle 'web.assets_frontend' */
odoo.define('shop_batch_sales.shop_batch_sales_add_to_cart',function(require){"use strict";var ajax=require('web.ajax');var core=require('web.core');var utils=require('web.utils');var _t=core._t;$(document).ready(function(){function price_to_str(price){var l10n=_t.database.parameters;var precision=2;if($(".decimal_precision").length){precision=parseInt($(".decimal_precision").last().data('precision'));if(!precision){precision=0;}}
var formatted=_.str.sprintf('%.'+precision+'f',price).split('.');formatted[0]=utils.insert_thousand_seps(formatted[0]);return formatted.join(l10n.decimal_point);}
$('#var-qty').on('click','a.js_add_cart_json',function(ev){ev.preventDefault();var $link=$(ev.currentTarget);var $input=$link.parent().find("input");var product_id=+$input.closest('*:has(input[name="product_id"])').find('input[name="product_id"]').val();var min=parseFloat($input.data("min")||0);var max=parseFloat($input.data("max")||Infinity);var quantity=($link.has(".fa-minus").length?-1:1)+parseFloat($input.val()||0,10);$('input[name="'+$input.attr("name")+'"]').add($input).filter(function(){var $prod=$(this).closest('*:has(input[name="product_id"])');return!$prod.length||+$prod.find('input[name="product_id"]').val()===product_id;}).val(quantity>min?(quantity<max?quantity:max):min);$input.change();return false;});function update_total_price(){var total=0.0;var $form=$('.p_variants').closest("form");var $total_price=$form.find('#var-total-price');$('.p_variants').each(function(){var $subtotal=$(this).find('#var-subtotal');var subtotal=parseFloat($subtotal.find('.oe_currency_value').html().replace(/\./g,'').replace(/\,/g,'.'));console.log('subtotal',price_to_str(subtotal));total=total+subtotal;});$total_price.find('.oe_currency_value').html(price_to_str(total));console.log('total111',total);}
$('.p_variants').find('input[type="text"][name="add_qty"]').on('change',function(ev)
{var $p_variants=$(this).closest('.p_variants');var add_qty=parseInt($(this).val(),10);var $subtotal=$p_variants.find('#var-subtotal');var $var_price=$p_variants.find('#var-price');var product_id=parseInt($p_variants.find('input[type="hidden"][name="product_id"]').first().val(),10);if(add_qty>0){ajax.jsonRpc("/shop/get_unit_price",'call',{'product_ids':product_id,'add_qty':add_qty}).then(function(data){var value=data[product_id];$var_price.find('.oe_currency_value').html(price_to_str(value));console.log('vvv',value,'vvv')
$subtotal.find('.oe_currency_value').html(price_to_str(value*add_qty));update_total_price();});}
else{$subtotal.find('.oe_currency_value').html(price_to_str(0));update_total_price();}});});});;






