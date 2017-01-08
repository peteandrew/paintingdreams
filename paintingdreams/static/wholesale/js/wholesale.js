function updateProductTotal(prodQuantityEl) {
  var quantity = Math.abs(prodQuantityEl.val());

  var itemPrice = prodQuantityEl.parent().prev().text().substring(1);

  var subTotal = quantity * itemPrice;
  if (isNaN(subTotal)) return;

  prodQuantityEl.parent().next().html('&pound;' + subTotal.toFixed(2));
}

$(function() {
  var subTotal = 0;

  $('table.wholesale_products input').keyup(function() {
    updateProductTotal($(this));
  });

  $('table.wholesale_products input').each(function() {
    updateProductTotal($(this));
  });

/*  $('form').submit(function(evt) {

    var errors = [];

    // Check required fields are set
    if (!$('input#id_shop_name').val().trim()) {
      errors.push('Shop name missing');
    }
    if (!$('textarea#id_shop_address').val().trim()) {
      errors.push('Shop address missing');
    }
    if (!$('input#id_contact_name').val().trim()) {
      errors.push('Contact name missing');
    }
    if (!$('input#id_contact_email').val().trim()) {
      errors.push('Contact email missing');
    }

    // Check at least one product added to order
    totalQuantity = 0;
    $('table.wholesale_products input').each(function() {
      totalQuantity += this.value;
    });

    if (totalQuantity < 1) {
      errors.push('No products added to order');
    }

    if (errors.length > 0) {
      var errorMsg = "The following problems were found with the submitted order:\n\n";
      for (var i=0; i<errors.length; i++) {
        errorMsg += errors[i] + "\n";
      }
      alert(errorMsg);
      return false;
    }

    return true;
  });*/
});
