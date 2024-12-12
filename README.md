# labelCutter
A tool to resize Royal Mail International Postage labels generated through eBay.

## Why is this needed?
I sell a lot of items on eBay and I use the integrated postage label purchase system.

I eventually bought a label printer which prints out postage labels using the A6 page size.

On eBay you get the option of regular A4 size labels or A6 for label printers.

This worked great for a while, that was until some genius decided to output all international labels as an A4 page, regardless of selecting the A6 size option.

This means that you can't print directly to your label printer.

Like many others, I would have to manually fix all the labels and feed them to my printer. This is time consuming and if you have to do something more than once, then you might as well code something to take care of it.


### Usage
python3 labelCutter.py label.pdf

This will output all labels in order to a PDF.