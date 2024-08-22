PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE article (
	id INTEGER NOT NULL, 
	title VARCHAR(100) NOT NULL, 
	content TEXT NOT NULL, 
	author_name VARCHAR(100), 
	author_occupation VARCHAR(100), 
	author_email VARCHAR(100), 
	author_description TEXT, display_on_index BOOLEAN, 
	PRIMARY KEY (id)
);
INSERT INTO article VALUES(1,'육식의 온실 가스 배출은 특별히 문제되지 않는다',replace(replace('  육식을 비난하는 사람들이 제기하는 가장 큰 문제는 소가 트림이나 방귀로 배출하는 메탄이다. \r\n인간 활동으로 인해 배출되는 메탄의 약 40%는 농축산업에서 비롯된다. 소의 소화 과정에서 메탄이 \r\n생성되는 것은 사실이므로 일견 일리 있는 주장 같다. 하지만 이산화탄소는 배출된 만큼 남김없이 \r\n대기중에 축적되는 반면 메탄은 상대적으로 수명이 짧아 대기 중에 축적되지 않는다. 메탄이 대기에 \r\n머무는 시간은 순간에 가깝기 때문에, 다른 온실 가스에 비해 온난화에 미치는 영향은 미미할 수밖에 \r\n없다. 따라서 온난화를 멈추기 위해 메탄 배출량을 급격히 줄일 필요가 없다. \r\n  게다가 소가 트림할 때 메탄을 배출하는 것은 사실이지만, 이것은 소의 소화 과정에서 자연스럽게 생긴 \r\n부산물일 뿐이다. 다른 온실가스와 달리 소가 배출하는 메탄은 자연 순환의 일부이기 때문에 환경에 나쁜 \r\n영향을 미치지 않는다.\r\n\r\n\r\n\r\n\r\n\r\n↳ <a href="http://152.69.224.69:5000/article/7">자연 속에서 순환하는 메탄</a>\r\n\r\n↳ <a href="http://152.69.224.69:5000/article/8">아마존 삼림과 소고기의 관계</a>\r\n\r\n↳ <a href="http://152.69.224.69:5000/article/9">목초지의 물 저장 능력</a>\r\n\r\n↳ <a href="http://152.69.224.69:5000/article/10">축산업의 회색 물 발자국</a>\r\n\r\n↳ <a href="http://152.69.224.69:5000/article/11">가축이 차지한 땅은 경작에 부적합하다</a>\r\n\r\n↳ <a href="http://152.69.224.69:5000/article/12">채식을 하면 오히려 경작지가 줄어드는 이유</a>','\r',char(13)),'\n',char(10)),'김경만','위스콘신 대학교 축산학과 명예 교수','jasonkim@wcu.edu','축산학 분야에서의 교육과 연구를 통해 학문적인 지식과 경험을 공유합니다.',1);
INSERT INTO article VALUES(2,'육식의 온실 가스 배출이 심각하다',replace(replace('소는 발효를 통해 먹이를 체내에서 처리한다. 이 과정에서 메탄이 생성되는데 트림이나 방귀를 통해 대기로 배출된다. 연구자들은 인간 활동으로 인한 메탄 배출량의 약 40%가 축산업의 직접적인 결과라는 사실을 확인했다. \r\n  대기 중 메탄은 수영장 안에 있는 물 두 컵 정도의 양이다. 게다가 메탄은 이산화탄소보다 대기 중에 머무는 시간이 훨씬 짧다. 하지만 메탄의 화학적 형태는 열을 가두는 데 매우 효과적이기 때문에 온난화에 미치는 영향은 이산화탄소보다 80배 강력하다. 대기에 메탄이 조금만 더 많아져도 지구 온난화에 큰 영향을 미칠 수 있다. 이미 비축된 이산화탄소에 비해 감축 효과가 바로 나타나는 메탄 배출을 급격히 줄여야 한다. \r\n  육식은 메탄을 많이 배출할 뿐만 아니라 메탄을 흡수할 삼림을 파괴하고 있다. 브라질은 상업용 목적으로 2억마리의 소를 사육하는 세계 최대의 쇠고기 수출국이다. 아마존에서 지난 6년간(2017~2022) 브라질 아마존 열대우림에서 8억그루의 나무가 베어졌다는 언론의 탐사보도가 있었다.\r\n\r\n↳ <a href="http://152.69.224.69:5000/article/7">자연 속에서 순환하는 메탄</a>\r\n↳ <a href="http://152.69.224.69:5000/article/8">아마존 삼림과 소고기의 관계</a>\r\n↳ <a href="http://152.69.224.69:5000/article/9">목초지의 물 저장 능력</a>\r\n↳ <a href="http://152.69.224.69:5000/article/10">축산업의 회색 물 발자국</a>\r\n↳ <a href="http://152.69.224.69:5000/article/11">가축이 차지한 땅은 경작에 부적합하다</a>\r\n↳ <a href="http://152.69.224.69:5000/article/12">채식을 하면 오히려 경작지가 줄어드는 이유</a>','\r',char(13)),'\n',char(10)),'최성빈','오하이오 주립대학교 환경과학과 교수','sbchoi@osu.edu','대기 오염과 지구 온난화에 대해 가르치며 대기 중 탄소 측정 및 처리 방법을 주로 연구합니다.',1);
INSERT INTO article VALUES(3,'육식이 물 낭비를 초래하지 않는다',replace(replace('최근 몇 년 새 소고기 산업이 유난히 물 낭비가 심하다는 비판의 목소리가 불거졌다. 한 연구에 의하면 소고기 1kg을 만들기 위해 필요한 물의 양은 약 10만 리터다. 또 물을 사용해 생산한 곡물의 대부분을 가축의 사료로 사용한다고 주장한다. \r\n   하지만 통계 자료에 의하면 한 해 생산된 옥수수의 10%만이 가축에 쓰인다. 게다가 물 사용을 계산하는 방식도 틀렸다. 앞서 제시한 논문은 소가 먹는 사료 1킬로그램을 생산하는데 1000리터의 물이 소비된다고 가정했다. 하지만 이 물의 약 92%는 빗물이다. 즉 소가 없었더라도 자연적으로 내렸을 비라는 뜻이다. 미국의 사료는 대부분 관개 없이 자연 빗물로 생산된다. 하지만 위의 수치를 대하는 사람의 대부분은 이 물을 인위적으로 끌어온 물로 생각하게 되어 물 낭비의 원인으로 소를 탓하게 된다.  \r\n  소는 물 낭비의 원인이 아니라 오히려 해법이다. 비가 농경지보다 목초지에 내리는 것이 생태계에 훨씬 유익하기 때문이다. 따라서 소를 키우는 목초지는 비가 별로 안 내리는 건조한 환경에서 특히 중요하다. \r\n\r\n↳ <a href="http://152.69.224.69:5000/article/7">자연 속에서 순환하는 메탄</a>\r\n↳ <a href="http://152.69.224.69:5000/article/8">아마존 삼림과 소고기의 관계</a>\r\n↳ <a href="http://152.69.224.69:5000/article/9">목초지의 물 저장 능력</a>\r\n↳ <a href="http://152.69.224.69:5000/article/10">축산업의 회색 물 발자국</a>\r\n↳ <a href="http://152.69.224.69:5000/article/11">가축이 차지한 땅은 경작에 부적합하다</a>\r\n↳ <a href="http://152.69.224.69:5000/article/12">채식을 하면 오히려 경작지가 줄어드는 이유</a>','\r',char(13)),'\n',char(10)),'하석주','산업 연구 및 농업 혁신 센터 이사','seokjuha@iaicenter.com','산업 연구 및 농업 혁신 센터에서의 이사로서, 혁신적인 연구와 산업의 변화를 이끌고 있습니다.',1);
INSERT INTO article VALUES(4,'육식이 물 부족을 부른다',replace(replace('물 발자국은 제품 생산 과정에서 직‧간접적으로 사용되는 물의 총량을 뜻한다. 소를 사육하기 위해서는 막대한 양의 물이 소요되는데, 연구에 따르면 식품 1kg 생산 시 소고기의 물 발자국은 채소의 50배에 달한다. 농축산업이 전체 담수 사용량의 70%를 차지하는데, 이는 대부분 육류에 사용된다.\r\n 연구에 따르면 미국 옥수수의 약 87%가 물이 부족한 지역에서 재배된다. 인위적으로 끌어온 물에 상당히 의존하는 것이다. 이런 취약 지역에서는 지하수를 끌어올려 사용한다. 현재 미국 옥수수 작물의 약 50%가 사료로 사용되며, 가축이 늘어남에 따라 사료도 더 많이 필요해질 것이다. 강수량이 적은 지역에서는 관개가 꼭 필요하며, 강수량이 많더라도 가뭄은 언제든 발생할 수 있다. 따라서 관개 면적의 비율은 계속 증가하고 있다. \r\n 물 발자국 중에서도 오염시킨 물을 정화하는 데 필요한 물의 양을 회색 물 발자국이라고 하는데 축산업은 특히 회색 물 발자국이 클 수밖에 없다. 따라서 육식은 채식에 비해 수질 오염에 큰 영향을 미친다. \r\n\r\n↳ <a href="http://152.69.224.69:5000/article/7">자연 속에서 순환하는 메탄</a>\r\n↳ <a href="http://152.69.224.69:5000/article/8">아마존 삼림과 소고기의 관계</a>\r\n↳ <a href="http://152.69.224.69:5000/article/9">목초지의 물 저장 능력</a>\r\n↳ <a href="http://152.69.224.69:5000/article/10">축산업의 회색 물 발자국</a>\r\n↳ <a href="http://152.69.224.69:5000/article/11">가축이 차지한 땅은 경작에 부적합하다</a>\r\n↳ <a href="http://152.69.224.69:5000/article/12">채식을 하면 오히려 경작지가 줄어드는 이유</a>','\r',char(13)),'\n',char(10)),'백승민','국제 환경 정책 연구원','smpaik@skfoundation.org','환경 정책과 관련된 연구를 수행하여 정책 제안과 실행 가능한 전략을 개발하고 있습니다.',1);
INSERT INTO article VALUES(5,'가축은 작물을 재배할 땅을 빼앗지 않는다',replace(replace('가축이 농경지의 3분의 2를 차지한다는 말을 들어봤을지도 모른다. 같은 크기의 땅에 토마토 22톤, 감자 24톤을 생산할 수 있는 반면 소고기는 약 100kg밖에 생산하지 못한다는 통계도 있다. \r\n 문제는 위 통계는 영양가가 같은 식품끼리 비교하고 있지 않다는 것이다. 동물 단백질의 칼로리는 탄수화물에서 얻는 칼로리보다 인간에게 훨씬 더 가치 있다. 소고기 160칼로리만 먹어서 얻을 수 있는 단백질의 양을 콩과 밥으로 얻으려면 600칼로리나 먹어야 한다. 따라서 같은 면적의 땅에 키울 수 있는 식량을 비교할 때 총 칼로리가 같은지 따질 것이 아니라 영양소의 양이 같은지 따져야 한다. \r\n 소를 없애버린다고 해서 작물 생산에 쓸 수 있는 땅이 더 생기는 것이 아니다. 더 늘어나지도 않을 경작지를 위해 소를 몰아내고 경작도 할 수 없게 되어버리면 오히려 장기적으로는 환경에 부정적인 영향을 미칠 수밖에 없다. 버려진 땅은 풀이 계속 자라고 식물 잔재의 축적은 결국 연료를 쌓아두는 것과 같아서 산불에 취약하게 되기 때문이다. \r\n\r\n↳ <a href="http://152.69.224.69:5000/article/7">자연 속에서 순환하는 메탄</a>\r\n↳ <a href="http://152.69.224.69:5000/article/8">아마존 삼림과 소고기의 관계</a>\r\n↳ <a href="http://152.69.224.69:5000/article/9">목초지의 물 저장 능력</a>\r\n↳ <a href="http://152.69.224.69:5000/article/10">축산업의 회색 물 발자국</a>\r\n↳ <a href="http://152.69.224.69:5000/article/11">가축이 차지한 땅은 경작에 부적합하다</a>\r\n↳ <a href="http://152.69.224.69:5000/article/12">채식을 하면 오히려 경작지가 줄어드는 이유</a>','\r',char(13)),'\n',char(10)),'이기준','애리조나 대학교 육우 유전체 연구팀','kijun.lee@arizonasu.edu','육우의 유전체에 대한 연구팀을 이끌고 있으며, 육우 및 육가공 식품의 영양소에 대해 연구하고 있습니다.',1);
INSERT INTO article VALUES(6,'가축이 땅을 차지하여 식량 효율을 떨어뜨리고 있다',replace(replace('채식과 관련하여 가장 흔한 오해는 채소의 영양소가 고기에 비해 부족하다는 것이다. 그런 주장을 하는 사람들은 고기에서 얻을 수 있는 영양소가 채소보다 훨씬 많으며 이를 전부 채소로 대체하는 것은 불가능하거나 막대한 손실을 초래한다고 강조한다. 그러나 실제 통계를 보면 가축은 농경지의 3분의 2 이상을 차지함에도 전체 칼로리의 18%, 단백질의 37%밖에 제공하지 못한다. 게다가 한 연구에 따르면 육류를 모두 채소로 대체할 경우 전 세계 인구에게 충분한 식량을 공급하면서 농경지를 75%나 줄일 수 있다. 미국, 중국, 유럽연합, 호주 영토를 모두 합친 것과 동일한 면적이다. 이렇게 줄어든 농경지를 자연으로 환원하면 생태계 회복에도 큰 도움이 될 것이다.\r\n 그뿐만이 아니다. 전문가들은 육식을 줄이고 식물 중심 식단으로 전환하면 목초지는 물론 논밭까지 줄어들 것으로 보고 있다. 고기를 덜 먹는 만큼 식물을 더 많이 먹어야 하니까 논밭이 늘어날 것 같지만 실제로는 그 반대라는 뜻이다.    \r\n\r\n↳ <a href="http://152.69.224.69:5000/article/7">자연 속에서 순환하는 메탄</a>\r\n↳ <a href="http://152.69.224.69:5000/article/8">아마존 삼림과 소고기의 관계</a>\r\n↳ <a href="http://152.69.224.69:5000/article/9">목초지의 물 저장 능력</a>\r\n↳ <a href="http://152.69.224.69:5000/article/10">축산업의 회색 물 발자국</a>\r\n↳ <a href="http://152.69.224.69:5000/article/11">가축이 차지한 땅은 경작에 부적합하다</a>\r\n↳ <a href="http://152.69.224.69:5000/article/12">채식을 하면 오히려 경작지가 줄어드는 이유</a>','\r',char(13)),'\n',char(10)),'최병주','캘리포니아 대학교 유기농 채식 식품 개발 연구팀','bjchoi@ucla.edu','유기농 및 지속 가능한 식품 개발을 통해 채식주의자들을 위한 건강하고 맛있는 대안을 제공합니다.',1);
INSERT INTO article VALUES(7,'자연 속에서 순환하는 메탄','먼 옛날 지구상에는 지금보다 대형 반추 동물이 훨씬 많았다. 소들은 그들 이전의 수많은 야생 반추동물들이 그랬던 것처럼, 메탄의 형태로 탄소를 공기 중에 방출한다. 이 탄소를 식물과 토양이 흡수하고, 이것을 다시 동물이 먹으면서 탄소가 대기로 돌아가고 이것이 다시 식물의 생장을 위한 원료가 된다. 이와 달리 화석 연료 배출은 생명 순환의 일부가 아니다. 땅속 깊이 있던 탄소를 억지로 뽑아내 불태운 것이다. 이렇게 방출되는 탄소는 식물, 토양, 동물, 대기, 다시 식물로 이어지는 자연순환 시스템에 전혀 보탬이 되지 않는다. 이것은 새로운 탄소이기 때문에 지구를 더 따뜻하게 한다.','박세광','국제 육류 산업 전문 컨설턴트','skkim@iccu.com','육류 산업에 대한 국제적 컨설팅을 제공하여 지속 가능성과 생산성을 향상시키는 전문가로, 다양한 기업 및 기관과 협력합니다.',0);
INSERT INTO article VALUES(8,'아마존 삼림과 소고기의 관계','소를 방목하기 위해선 넓은 토지는 물론 막대한 양의 곡식이 필요하다. 소를 방목하고 사료를 재배하기 위해 브라질의 열대우림이 개척되는 중이며 1초에 약 4000제곱미터 가량의 열대우림이 현재도 파괴되는 중이다. 환경단체의 보고서에 따르면 약 17~20% 아마존 삼림이 이미 파괴되었으며 벌채된 지역은 대부분 소떼를 키우는 목장이 되었다고 한다. 1960년 이후 약 90만 제곱킬로미터 이상의 삼림이 가축 목초지로 바뀌었다는 보고도 있었다. 기업들은 공무원들을 매수하여 땅을 태울 수 있게 허가를 받거나 불법으로 불을 질러 목초지나 가축 사료 경작지를 확보한다. 이 과정에서 엄청난 양의 탄소가 배출되며 수많은 야생동물이 죽고 생태계가 파괴된다.','김지호','채식주의 컨설턴트','jiho.kim@govegan.org','채식이 건강과 지구 환경에 미치는 영향을 조사하고 인간과 동물 모두에게 유익한 채식 방법을 연구합니다.',0);
INSERT INTO article VALUES(9,'목초지의 물 저장 능력','농경지와 비교해서 목초지는 토양침식률이 80%까지 감소하고 수질이 현저히 향상될 수 있다. 수분 유출에 있어서도 물이 건강한 초지를 통과할 때 방지 효과가 가장 크다. 경작지의 물 유출률과 토양침식률이 목초지보다 훨씬 높다는 연구 결과가 있다. 즉, 경작지에서 물과 토양이 훨씬 많이 손실된다는 의미다. 소가 이용하는 물의 약 30%는 소의 오줌과 거름의 형태로 초원으로 돌아간다. 그 과정에서 양분과 미생물이 초원에 추가된다. 땅 밑에서 미생물이 충분히 활동할 때만 빗물이 토양의 상위층을 침투할 수 있다. 잘 관리된 목초 사육 시스템에서는 토양이 스펀지처럼 빗물을 흡수하고 식물 뿌리가 물을 빨아들인다.','차현범','국제 지속 가능 사육 환경 설계 연구팀','hbcha@msinst.com','지속 가능한 사육 환경을 설계하고 개선하는 전문가로, 동물 복지와 환경 보호를 고려한 사육 시스템을 개발하고 있습니다.',0);
INSERT INTO article VALUES(10,'축산업의 회색 물 발자국','회색 물 발자국은 오염시킨 물을 정화하는 데 필요한 물의 양이다. 축산업은 회색 물 발자국이 큰 대표적 산업이다. 가축의 사료 생산을 위한 옥수수와 대두 농작물에 사용된 비료와 살충제의 유출로 인해 수질 오염이 발생한다. 합성 비료는 담수 및 해양 시스템을 오염시키는 원인 중 하나다. 또한 오늘날 대부분의 축산업은 공장식 밀집형 축사를 이용한다. 한 장소에 많은 가축이 밀집해 있어 분뇨의 양이 토양이 수용할 수 있는 수준을 넘어선다. 분뇨 뿐만 아니라 항생제, 박테리아, 병원균 및 중금속도 배출된다. 이를 정화하려면 막대한 양의 물이 필요하다.','박주민','뉴욕대 지구과학과 교수','jmpark@nyu.edu','기후 변화와 수질 오염의 관계에 대해 연구하고 있습니다.',0);
INSERT INTO article VALUES(11,'가축이 차지한 땅은 대부분 경작에 부적합하다','전 세계적으로 농경지의 60퍼센트 이상이 경작 농업을 시도하기에는 바위가 너무 많거나 가파르거나 건조한 목초지와 방목장이다. 농경지의 유용성을 따질 때는 여러 가지 요소를 고려해야 하는데 그중 한가지가 해당 지역이 강우나 관개 시설에 의존하는 작물을 재배하기에 적합한지 살펴보는 것이다. 목초지는 대부분 관개 시설에도 적합하지 않다. 그래서 목초지 대부분은 작물을 재배하기에 적합하지 않으며 애초에 일부 유형의 목축에만 적합하다. 즉, 경작 농업을 할 수 없는 곳에 소를 키운 것이며, 소를 몰아낸다고 이 땅에 작물을 재배할 수 있는 것은 아니라는 의미다.','김민석','국제 육류 공급망 효율화 전문가','victorkim@wholefoods.com','육류 공급망을 효율화하고 지속 가능한 공급망을 구축하기 위해 노력하는 전문가로, 혁신적인 방법과 전략을 개발하고 있습니다.',0);
INSERT INTO article VALUES(12,'채식을 하면 오히려 경작지가 줄어드는 이유','축산업에 사용되는 목초지는 전체 농경지의 절반 이상을 차지한다. 그런데 나머지 농경지 중에서도 43%는 가축에게 먹일 사료를 재배하는 데 사용된다. 현재 농경지 가운데 인간이 먹을 작물 재배에 사용되는 면적은 일부에 불과하다. 육식을 줄이면 그만큼의 식량을 대체하기 위해 인간이 먹을 작물 재배가 늘어나고 이에 따라 작물 재배를 위한 논밭은 증가한다. 하지만 가축의 사료를 위해 재배되던 작물의 논밭이 그보다 더 많이 줄어들기 때문에 총 논밭의 면적은 줄어드는 효과가 발생한다.','이수환','환경 보호 및 채식주의 컨설턴트','shlee@greenpiece.com','식품 소비의 환경적 영향과 지속 가능한 식습관을 위한 컨설팅을 제공하고, 기업과 정부에서 지속 가능한 식품 생산을 촉진합니다.',0);
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(255) NOT NULL, 
	password VARCHAR(255) NOT NULL, article_order VARCHAR(255), 
	PRIMARY KEY (id), 
	UNIQUE (username)
);
INSERT INTO user VALUES(1,'admin','123','[1, 4, 2, 5, 6, 3]');
INSERT INTO user VALUES(2,'munji','1111','[4, 3, 2, 1, 5, 6]');
INSERT INTO user VALUES(3,'110909','11','[2, 4, 3, 5, 1, 6]');
INSERT INTO user VALUES(4,'20240209','11!!','[3, 4, 6, 1, 2, 5]');
CREATE TABLE rating (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	article_id INTEGER NOT NULL, 
	rating INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_rating_user FOREIGN KEY(user_id) REFERENCES user (id), 
	CONSTRAINT fk_rating_article FOREIGN KEY(article_id) REFERENCES article (id)
);
CREATE TABLE visit (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	article_id VARCHAR(255) NOT NULL, 
	start_time VARCHAR(255) NOT NULL, 
	end_time VARCHAR(255) NOT NULL, 
	duration INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_visit_user FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO visit VALUES(1,1,'4','2024-04-27T04:49:08.120Z','2024-04-27T04:49:21.086Z',12966);
INSERT INTO visit VALUES(2,1,'11','2024-04-27T04:49:21.131Z','2024-04-27T04:49:30.910Z',9779);
INSERT INTO visit VALUES(3,1,'5','2024-04-27T04:49:39.066Z','2024-04-27T04:49:51.885Z',12819);
INSERT INTO visit VALUES(4,1,'7','2024-04-27T04:49:52.005Z','2024-04-27T04:49:53.502Z',1497);
INSERT INTO visit VALUES(5,1,'5','2024-06-20T00:27:10.168Z','2024-06-20T00:27:11.870Z',1702);
INSERT INTO visit VALUES(6,1,'1','2024-06-20T00:49:01.795Z','2024-06-20T00:49:03.759Z',1964);
INSERT INTO visit VALUES(7,1,'12','2024-06-20T00:49:03.954Z','2024-06-20T00:49:05.466Z',1512);
INSERT INTO visit VALUES(8,1,'1','2024-06-20T00:49:05.495Z','2024-06-20T00:49:06.350Z',855);
INSERT INTO visit VALUES(9,1,'1','2024-07-01T11:39:00.275Z','2024-07-01T11:39:02.098Z',1823);
INSERT INTO visit VALUES(10,1,'12','2024-07-11T08:18:50.452Z','2024-07-11T08:18:51.234Z',782);
INSERT INTO visit VALUES(11,1,'12','2024-07-11T08:24:35.040Z','2024-07-11T08:24:35.748Z',708);
INSERT INTO visit VALUES(12,2,'3','2024-07-30T11:21:28.649Z','2024-07-30T11:21:45.809Z',17160);
INSERT INTO visit VALUES(13,1,'1','2024-07-30T11:24:48.586Z','2024-07-30T11:25:01.245Z',12659);
INSERT INTO visit VALUES(14,3,'1','2024-07-30T11:26:11.483Z','2024-07-30T11:35:33.189Z',561706);
INSERT INTO visit VALUES(15,1,'1','2024-07-30T11:35:40.353Z','2024-07-30T11:35:44.705Z',4352);
INSERT INTO visit VALUES(16,1,'1','2024-07-30T11:37:06.179Z','2024-07-30T12:15:36.532Z',2310353);
INSERT INTO visit VALUES(17,4,'3','2024-07-30T12:38:53.107Z','2024-07-30T12:42:43.750Z',230643);
INSERT INTO visit VALUES(18,4,'12','2024-07-30T12:42:43.844Z','2024-07-30T12:42:59.518Z',15674);
INSERT INTO visit VALUES(19,4,'3','2024-07-30T12:38:53.107Z','2024-07-30T12:43:02.398Z',249291);
INSERT INTO visit VALUES(20,4,'11','2024-07-30T12:43:02.484Z','2024-07-30T12:44:06.466Z',63982);
INSERT INTO visit VALUES(21,1,'6','2024-08-14T03:19:22.126Z','2024-08-14T03:19:29.291Z',7165);
INSERT INTO visit VALUES(22,1,'4','2024-08-14T03:19:45.937Z','2024-08-14T03:31:16.808Z',690871);
CREATE TABLE read_article (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	article_id VARCHAR(255) NOT NULL, 
	author_info_clicked VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_read_article_user FOREIGN KEY(user_id) REFERENCES user (id), 
	UNIQUE (article_id)
);
INSERT INTO read_article VALUES(1,1,'4','0');
INSERT INTO read_article VALUES(2,1,'11','1');
INSERT INTO read_article VALUES(3,1,'5','0');
INSERT INTO read_article VALUES(4,1,'7','0');
INSERT INTO read_article VALUES(5,1,'1','0');
INSERT INTO read_article VALUES(6,1,'12','0');
INSERT INTO read_article VALUES(7,2,'3','0');
INSERT INTO read_article VALUES(8,1,'6','0');
CREATE TABLE memo (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	article_id VARCHAR(255) NOT NULL, 
	content VARCHAR(1000) NOT NULL, 
	timestamp DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_memo_user FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO memo VALUES(1,1,'4','123','2024-04-27 04:49:18.435849');
INSERT INTO memo VALUES(2,1,'11','456','2024-04-27 04:49:27.795839');
INSERT INTO memo VALUES(3,1,'5','나임','2024-04-27 04:49:48.781976');
CREATE TABLE feedback (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	article_id VARCHAR(255) NOT NULL, 
	feedback VARCHAR(1000) NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_feedback_user FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO feedback VALUES(1,1,'11','없음ㅇㅇ');
INSERT INTO feedback VALUES(2,1,'7','나임123');
INSERT INTO feedback VALUES(3,4,'11','ㅜ');
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('7c450b250865');
CREATE TABLE article_display (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	article_id INTEGER NOT NULL, 
	position INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(article_id) REFERENCES article (id)
);
COMMIT;
