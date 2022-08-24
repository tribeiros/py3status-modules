"""
Bitcoin price
This module request bitcoin price on coinbase and displayed on py3status;

Color options:
    color_low: for the price lower threshold
    color_high: for the price above threshold

Requires:
    babel: library to converter integer to currency

Example:

```
bitcoin {
    color_low = '#000fff'
    color_high = 'fff000'
}
```

@author Tiago Ribeiro
@license GPLv3
"""

import subprocess
import babel.numbers

class Py3status:

    def _notify(self, price):
        currency = babel.numbers.format_currency(price, "USD", locale='en_US')
        subprocess.run(["notify-send", "-u", "normal", "-t", "30000","bitcoin", currency],check=True)

    def _req_bitica(self):
        try:
            url = "https://api.coinbase.com/v2/prices/spot?currency=USD"
            req_data = self.py3.request(url).json()
            json = req_data['data']['amount']
            price = json.split(".", 1)
            return price[0]
        except self.py3.RequestException:
            msg = 'bitcoin'
        return msg
    
    def response(self):
        price = self._req_bitica()
        currency = babel.numbers.format_currency(price, "USD", locale='en_US', format=u'#,##0.##', currency_digits=False)
        x = int(price)

        if x > 22000:
            color = self.py3.COLOR_HIGH
            self._notify(price)
        else:
            color = self.py3.COLOR_LOW

        response = {
            'full_text': currency,
            'color': color,
            'cached_until': self.py3.time_in(600)
        }
        
        return response

if __name__ == "__main__":
    
    colors = {
        'color_low': '#ffffff',
        'color_high': '#000000'
    }

    from py3status.module_test import module_test
    module_test(Py3status, config=colors)