$(function() {
  var subTotal = 0;

  function updateProductTotal(el) {
    var quantity = Math.abs(el.val());

    var prodPrice = el.parent().prev().text().substring(1);

    var prodTotal = quantity * prodPrice;
    if (isNaN(prodTotal)) return 0;

    el.parent().next().html('&pound;' + prodTotal.toFixed(2));

    return prodTotal;
  }

  function updateTotals() {
    subTotal = 0;
    $('table.wholesale_products input').each(function() {
      subTotal += updateProductTotal($(this));
    })
    $('table.wholesale_subtotal td:nth-child(2) span').text(subTotal.toFixed(2));
  }

  $('table.wholesale_products input').keyup(function() {
    updateTotals();
  });

  updateTotals();
});
