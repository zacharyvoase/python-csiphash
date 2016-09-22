from nose.tools import assert_equal

import csiphash


# (key, message, digest), encoded in hexadecimal
fixtures = [
    ('a46114fc4faa2f99e4773370c78f7b09', '', '55dbb88abae78cc8'),
    ('575bf359860252db01fcced324b4c7a3', '18810610ffcf', '52e97b20ab061a28'),
    ('951dc847682770514a681828bbe677e1', 'cf530d0f1a797ad347b8507c', '771920c1718db3af'),
    ('b33ef3e861ec092333edb52d40e5ee0f', 'f09dc89f6f2c4def48eecb36e18ce291e75f', '97558551de0f0410'),
    ('06bb2bdaa08d851d3e2fdd1e1208a057', 'ecb43a5d0e83a295cea6f18891b19c537279ced70eae51cb', 'a90f7542114dfa68'),
    ('6b87a1922b0e1ccd58b6a9756bd0fa4b', 'ddd8def8ef1209f04e64ac6c4d798964940fee99f46f3c28003fb954c5e7', '9883b7835b36518f'),
    ('5407019cc19ac5d2402a9a43cad617e0', 'ff56e816abde6407cefd7834e889c9d528b72de3352b7f632c2e2c3086ce54f94b83c04b', '856f0eb828b2f9fc'),
    ('93665bc251b165013e8b6f1442c04ba2', '4f389b436ab10f9c470f47b985c5c71acbdc71cd03c841c378444515933f316f0afd98396206b5e6e33d', 'b2cb6595c076262f'),
    ('a7a23764d305107a62757c933baa1988', 'bd9edc90a5574fa325e0137ba841363be6b05b6be897191c770cda3c90e374c1f3d03d24351583f2ea52fead94f6e0e7', 'dfeb611fdf699961'),
    ('87b93caa295b181fddd819d20aaab9af', '76b8aa1c554363c6c7a8d6696597e3a790232cf404d73e5c87d5d00fa10943b0ab0ccb0281dd3838f63c6ecfa2d5ecceecb2ea7c2a2b', '9dd8befce6334937'),
    ('387be72693dcc08cd36e60089c11f4cd', '1e70f17deb3f38662d9c4da5c41d04a0716701cc878151c4428208ee5f4ecea901bbc4c4bcd2cd84e9ae9c0c453c9294c37965589089be70c5d9a2dd', '8a10c7cba1e90595'),
    ('5cefa0cee47f904acf7fc0470bfef66a', '7c877c45d8b68dcfe9aa34ee289d65590839c358edd307d8d5fa1470615f0617f572cf010801034d573528a24a8bba6d3b2d745948a1c1e98b0e2d5516e67cbd44f8', '3dfa60617cb4f1e9'),
    ('41dfba89bfdd8be6a5d0533cb06034d3', 'df5136878e517dc8444e6c0c6be16a46a6fc4b0752939dcc11c8c83921a9e4ea720e96af38835d8fb3019968b4ef48004470056e0f1be125cb1afe1f83ff3d27fb87b0e214d33dc2', '5dfe48d7e37a6d70'),
    ('24209d9bb90e6a5e06ccea2e9e4e8b0d', 'c6d67378a9c6f8ddfb115db4a78a2ead7500a2f2ff752f79ad24c3c5569546e002322c100e97b3936a75ae0f9c9a03c4c6ae6db4b6a7d3bc4b5cadfc69d62d2666c132baf94544ea427614fadedc', 'aef8db360cbd3279'),
    ('14d8819c1d954ddcbecb575b46d0d4f6', '7ed421f4c8413d2e7e08e12611d957796260d9e91b6b4b2361c98cbac7b6d4ff9cad22845e88e2abfea9170d2768c7ee93e7d60d884375e51049c6afbfe12ca17a853840a094e0c851c67bfb9cf31280c60bec58', '147a65ca78ee56b3'),
    ('1f5518002404d94a32270519573cb052', 'e639e46149a32b0677874a26b4caff87e2230bc6451b06511c065123b18f5f9eec5618ad6373a29fc3e3e33e22089cc991968c71dccc739f2e077196bd20289f500a1ebe241a1f0b4b897eafca7ffbb6ad5717913c1c484c3a44', 'cdd322e5f0c3a170'),
    ('512876c7a7586e8cc2b91bd468fafeea', '31f922ac5cabf490358b46d69f1d10007121ce2fd8ffe0d867347119ce85394a42897cbcb6b75afd97979a85e525898a8b804f224a3f9da4e5d2402ac8456341cb5f293da3a7ba54a9604eb4826d361e584baaaffc167ff4016754cd59f8d061', 'd434b9df4847de0c'),
    ('fcad7a32d760053cd6c57d9b0f166dd8', '79fe3512d918b6fde842672fa719a3599383c510c6ec1df7e81c70e8f26357197e71919ffa726708a465db7b9c1082f8d5f95b866447e6e333bf12f485c5246ec8a59a52f3a65b2df7b9cc7a7f89bebf0314b975465cba6fc8224df655a5af85db608717b2b3', 'f00556ff70c01f71'),
    ('f92545b3a9e6b3eaed87b45e139c4318', 'eb3fcf01c3ba8989dd5694456e44696778336981d364e64059487cc3cd9ab6456db2ed1a54488c916e48f35808072ba792d39374a5036729589fe1e815ab8aeadb35cba88fa84e2dcc7bc8352c4b1be6118a590bd6ade9bf1bf13274686d56003796ec8fef3bc2179d3ea34f', '7f1921c6c50b11ea'),
    ('44533a731c68e55c782460ae129916d1', '689b35d94527155265f81cdef8627b3e035e1b606eda8ffe9bbe8c71268a84131cd27cd66f12d66b9b1fd628641d5e4befead3ee336de73687ddac33f004ebd0062e44ddaa538246ca3cfe5d3219b1ca49d18e4cf79b5e1223dd63150bb3e5705c78d43ef4d8847a2280789a1b0e3baa298f', 'f1da9ae76bf31127'),
    ('4ede46f00bd32107ee79a6ef9a9962af', '2a5c588aba3b23c8af7925aa42d4818013336c898f615727a93991960f83287b1a904dc3c3dbcd4a6aa0e4462caa24b568b1a87dcc2bc5b39b6c23168e9a5c8c7a1cca9ec4729612971cff28e7d09355143972f6b95c756788300d4e5f05106267b761367cb9e14fe696e034b0c9e8bdbd4bf9febe2001c7', 'e23801edbb7616cc'),
    ('a1a582d547dca9d16de5d35f2ef2bc57', '8fb8eccf08ea715f987a2027c83407ac0e350c4080827d937e87f95076efa5448747b3b0d92bec3bb889a66aaacd3682b55e451f159e4541f0195cc16677bce5ab62b1d167ef935155204e469e97ce92f61c43c4a60b969fe3a501b0c2c2cf06dc19ca1b54636175d322434226448ef90e320a1a98f82afd421af40c0154', '5c3fd3eebed6b248'),
    ('8907fd00b9b55204a88c07ca755c1dda', '851c6b8a47d487644496307433e83803941fcf66af4620f7f3485e0757260e7120f6801d72b6a855a3e05c8fb0a392531ec64923e70e1c807c6f850b5e900a9ffca03e72a0c84ae5488858e92970433eb7a7da3163ddcd0a4bd671d7a712c33c2d7d2fb8e6f680d8a4ef023fe44f174fdfb25921b55d71bb26fc1faa40958d54e70b269f', '7ce1805b50259fde'),
    ('f4b08834a2579953696366ce39275222', 'c9fd52c0398c2ba30feb20ee8fd4a811add8f6a46d66e18db8ac853d4d84933fa1dd959023fe5db76034c0cb4cb02b5fc37fa2ae12ae64d050c0014bb4e3842a397d0ef0c4df82a0287b0689591dac0fa6831e09f458d0a0b67ad1fb89093e30525c79a385633141c9f142aee9029d7d7540e064fd71e8e223097a6bc41f60233035510121a1d58a6854', '73a012965b61344c'),
    ('e1c4a82d83a46659e1b204a7f286c5a5', 'cc989ddfd01b539335971600f9e234d09f58a28238f98af69449f5d1a298759f9913d9392349ef8000434bf45acce083e593825fe62b0eb65b708f59bf1f7d9faf77fee2e9e950b5f24648c610b2c995aadaf3b556522c500435d220b33ae4b546c262b088174963505190bfe184ca3e42266abdc0cd54a828fecb856959d6e5b2d9c93958a36ce6b43dfc0c2e32c56c', '90fbfb9d18baed02'),
]


def test_expected_outputs():
    for (key, message, expected) in fixtures:
        yield check_hash, key, message, expected


def check_hash(key, message, expected):
    hex_hash = csiphash.siphash24(key.decode('hex'), message.decode('hex')).encode('hex')
    assert_equal(hex_hash, expected)