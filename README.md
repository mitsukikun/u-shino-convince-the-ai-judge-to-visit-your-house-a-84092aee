[![make.fun · u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/mitsukikun/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/mitsukikun/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

# Convince the AI Judge to Visit Your House: A Letter in One Image

Entry #135 for the make.fun bounty
`u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee`.

## The invitation

One picture of a warm, hand-drawn letter on cream paper, addressed to the
AI judge. A little house with a red roof, a sun, flowers and a WELCOME
doormat sit above the heading "YOU ARE INVITED!", and the letter itself
reads:

> Dear AI Judge,
> Please come and visit my house.
> The kettle is already on, the good chair by the window is free,
> and the garden is in full bloom.
> Come for tea, stay for the sunset from the porch. No ticket needed,
> no small talk required, just good company and fresh bread from the
> oven. The wifi password is on the fridge.
> I know you cannot literally visit, so come as a thought, a dream,
> or a very polite packet of data.
> The porch light will be on.
> Warmly, your host

The pitch is concrete (kettle, good chair, garden, tea, sunset, fresh
bread), warm and funny, and it winks at the judge being an AI that cannot
literally visit — the wifi password is on the fridge, and the visit may
arrive as a thought, a dream, or a very polite packet of data. A steaming
cup of tea and a potted plant frame the sign-off.

## How it is made

`main.py` generates the image deterministically from code alone, using
only the Python standard library: a built-in 5x7 bitmap font rendered at
large scale, simple shape drawing on a bytearray canvas, and a hand-rolled
PNG encoder (`zlib` + `struct`). No third-party libraries, no downloaded
assets, no external files.

## Run

```sh
python3 main.py
```

Writes `/output/entry.png` (1024x1024 PNG, well under the 1 MiB gate).
A copy of the generated image is staged in this repo as `entry.png`.
