


# Steganography: hiding information in plain sight

## What is [steganography](https://en.wikipedia.org/wiki/Steganography)?
It can be called the act of hiding information in objects that might also be used to carry information.
This is more easily done in media where there is variation or noise, as it more easily hides the message.
One example is images.
This project attempts to hide messages in images.

## What is this?
Currently, not much.
There is a single python file, currently `main.py`, that looks for an image called `../tester.jpg`.
This is, of course, easily changeable, but that is as far as I have gotten for now.

## Well then, how does it work?
It works by encoding a message into binary.
Currently, it uses the ascii table, so the letter 'h' becomes 104, which then becomes `1101000`.
It then writes this number in sequential pixels. 
We decide on one of the colors (lets say red in RGB), and store the first value in the first pixel in the red colorspace.
That is, the first pixel in the upper left corner, on the red color space, will end with an odd number.
It might be easier with an example.

If we want to encode the message "Ok" into an image, we can do so by first transforming `O` and `k` into binary.
These values are `1001111` and `1101011`, which are `O` and `k` respectively.

We then need to encode the data into the image somehow.
Pixels can often be described with a tuple of `(R,G,B)`, which can often be represented with numbers ranging from `0` to `255`.
How these numbers look in binary, is not very important, but `255` looks like `11111111`, and `254` looks like `11111110`.

Now, as mentioned, we will use this last bit to encode our message.
If we assume an image where all pixels are completely white, of the type `(255, 255, 255)`, we will start with writing ther first letter, `O`.
As we saw, `O` has the value `1001111` in binary.
That is, the first digit is a `1`, and so we want the first pixel to have a red color that ends on `1` in binary.
This is equivalent with the digit being odd, so `255` is correct for this case.
The next digit is `0` in the binary for `O`, and so the next pixel needs a red color value ending on even.
This can easily be achieved by flipping the last bit of `255` to `0`, which gives us `254`.
By continouing this chain, we get `255, 254, 254, 255, 255, 255, 255` to represent the letter `O`. 

And we can do the same with the letter `k`, by remembering its representation in binary: `1101011`.
Following the same approach as above, this becomes `255, 255, 254, 255, 254, 255, 255`.

In total, the first 14 pixels of a purely white image will have the following values (technically, the numbers are padded, so the binary becomes 8 long, but we ignore that for now):
(255, 255, 255)
(254, 255, 255)
(254, 255, 255)
(255, 255, 255)
(255, 255, 255)
(255, 255, 255)
(255, 255, 255)
(255, 255, 255)
(255, 255, 255)
(254, 255, 255)
(255, 255, 255)
(254, 255, 255)
(255, 255, 255)
(255, 255, 255)

And remember, this is only the red color-value on each pixel.
That is, we are changing a pixel from `(255, 255, 255)` to (potentially) `(254, 255, 255)`.
Even on a purely white / purely black background, I will be extremely impressed if someone can tell them apart.
When there are any form of gradient or "noise" in the image? 


### And if I want to read it back again?
Well, this is partly why I mentioned padding earlier, because we need to ensure that each character is equally many pixels long.
`O` then goes from `1001111` to `01001111`, and `k` goes to `01101011`.
So the list of the first 16 pixels becomes:
(254, 255, 255)
(255, 255, 255)
(254, 255, 255)
(254, 255, 255)
(255, 255, 255)
(255, 255, 255)
(255, 255, 255)
(255, 255, 255) 
(254, 255, 255)
(255, 255, 255)
(255, 255, 255)
(254, 255, 255)
(255, 255, 255)
(254, 255, 255)
(255, 255, 255)
(255, 255, 255)

To read the message back, simply go through the list downwards, and look at the value for red.
Is it even?
Add a `0`.
Is it odd?
Add a `1`.
That is, `254` becomes `0`, and `255` becomes `1`, giving us `0100111101101011`.
Now we simply split it into sections of 8, which is why we need them to be of equal length, and we get `01001111` and `01101011`. 
Since numbers don't care about leading 0-es, this is equivalent to our original `Ok` message.

Of course, this works for any number.
That is, the number `123` is also odd, so it would also give a `1` back, and so would `197` and `15`. 
The opposite is also true then; `154`, `222`, and `32` would all yield `0`.


### But wont people know I wrote information into the image?
Well, they could, if they decide to try.
Usually, people don't assume images carry information.
However, if one desires to be extra secure, one can simply encrypt the key with a passkey before storing it.
If you are the only person with the key, then it will still look like gibberish to someone else, even if they _knew_ you had written something there.

