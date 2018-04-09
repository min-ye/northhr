$(document).ready(function() {
 
   var video_panel_height = $("section.video").height();
   var intro_panel_height = $("section.intro").height();

   var height = (video_panel_height > intro_panel_height) ? video_panel_height : intro_panel_height;
   height = height + 25;
   
   $("section.video").height(height);
   $("section.intro").height(height);
   
   var information_panel_height = $("section.information").height();
   var product_panel_height = $("section.product").height();

   var height2 = (information_panel_height > product_panel_height) ? information_panel_height : product_panel_height;
   
   $("section.information").height(height2);
   $("section.product").height(height2);
   
   var import_product_panel_height = $("section.import-product").height();
   var export_product_panel_height = $("section.export-product").height();

   var height3 = (import_product_panel_height > export_product_panel_height) ? import_product_panel_height : export_product_panel_height;
   
   $("section.import-product").height(height3);
   $("section.export-product").height(height3);

   var import_tax_panel_height = $("section.import-tax").height();
   var export_tax_panel_height = $("section.export-tax").height();

   var height4 = (import_tax_panel_height > export_tax_panel_height) ? import_tax_panel_height : export_tax_panel_height;
   
   $("section.import-tax").height(height4);
   $("section.export-tax").height(height4);
});