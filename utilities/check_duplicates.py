#!/usr/bin/env python3

tokens = [
    "701fad0f88fd531097ef46865420b5d2ba34e99d",
    "51e000717f3ae90af9948fe8fd2d4d2fe1ca8315",
    "d16cbafa350ff517a3975d4f68b9777766fc51a3",
    "901ad96c5bd5a5fd0e370b497c915bd26fdb7b95",
    "2e58617495aa51eb80a34439bcd584291f0ca922",
    "e96754554412f10ca4e45e69a7a473d1126150ff",
    "2a82ebfefffd335e07fd582f23f76bbe13750437",
    "2bb79f81523bf55e230d33a6ba9964dd6dcbc8bb",
    "9235da0e952445c7e81bf093a24a0d6361d0eda2",
    "a1df028f81fc9a264486c794368ea816baafba1e",
    "e850be7e21c33c3d916d041accf34dbab2a7ea40",
    "715ac3da96291d0adf48d99680d3bc66c151bf66",
    "5553e659128f58c0fef8a7f95747a5b567e16108",
    "3f0eac8e1fb50b14c9927be3b72c7f3bdfb4c05a",
    "b7eb3ae281e35b496353fd2525779d6f05ae5a67",
    "165d18c6960207ab5a3ec270114c37539e986b89",
    "21bcf3ba8a1bd49b1e0dc66c422fd25d0eb61bd7",
    "20b23fd8517df4c07777cce7f7715ca29e8b3cdf",
    "b193f43c4959e2fcd7343735c9eda3238e44b4e4",
    "e6f426d13bf57b1119e774506b4d513b12f7a7d3",
    "68617fbcc8781f0cdfa8e5542b7498451424e261",
    "0efb6b520178df53240b9cceee0720f1e67caf41",
    "92f924466b39a3863260c12cec665e9ade4a8a0f",
    "fc6fbfcf4fb171ee3ea648d05be9b59b382b9a51",
    "1637a5caddede416428b1e6d39da42c7a96e2b1b",
    "b6b952406ef33a6af2c1449d1662b20cd10d1c4f",
    "dd7416d4f8105ca27042055017c2c1daff76b844",
    "688f883cfc4a7750bf90f899213b2bbfc3ae40c6",
    "c01c82d6fbaaac67971067072d2b4b375e442e00",
    "f2933f331496d18376ead55084c7c55368f57714",
    "eedccb348b0000e0a9a9691ac2ed363fa5cb9a1b",
    "59aa213a93fffcb86faffcc2df2654386b36f0ef",
    "82c12015452f7675aed82a0acf6540ab673726e9",
    "8ccbc3ac21ace66be87833ed2f2e79fdff93ace1",
    "1f5e77bac60f10cc82c86b485e191c3e846eb4b5",
    "0cf536c02eb1ef0d2d17a612fb06107530f6062d",
    "20a21c3fb8fb2e7e761d6a1b8a0ad26f71a41b04",
    "b2b95c2ac08f84d38f5f75546acdcde8e079435e",
    "1570deceab17adb1b2fc83279f7fba87ed0895b6",
    "f77fe5b03aac324377cd788b3c87ad95f6208998",
    "c9ec7a1f7b168a049f503a1baf771265933c1fe6",
    "c9e2c677123f4a4f8a2fbe79fe9cf68d12c1cf97",
    "757e53721f852d0456ef572981725ac9b0431909",
    "e80719fac75abf742986f47c5d10440a931f6c02",
    "c715d27c85f61ff05fe1ecae5a4d6ab6ca857ca2",
    "84a9c436ad089d1739e68e2a051b255f4bdf9144",
    "1e2ab67cd20a264b4efd43281c78fcd30904c5db",
    "80103ea68b62115fbbde9b9f65b4cdb063ad7693",
    "d51f2166b808736fb2f846e986c42601b37e114e",
    "0b8c19bc8f874b8155e77708d078e43a7e2fc8c4",
    "785dfb24752099ed4a0de9f92d377103dd61a0dd",
    "917227a7f55bea8c001fa65211db37b7f39dbe73",
]

print(f"Total tokens: {len(tokens)}")
print(f"Unique tokens: {len(set(tokens))}")

if len(tokens) != len(set(tokens)):
    print("\n🎯 DUPLICATES FOUND!")
    from collections import Counter
    counts = Counter(tokens)
    for token, count in counts.items():
        if count > 1:
            print(f"Token appears {count} times: {token}")
else:
    print("\n❌ No duplicates found - all tokens are unique")
    print("\nThis means the token generation has sufficient precision.")
    print("The vulnerability must be exploited differently...")
