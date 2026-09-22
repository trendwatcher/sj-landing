/** 사이트 전역에서 쓰는 정보. 바뀌면 이 파일만 고치면 됩니다. */
export const SITE = {
	name: '김세진 소상공인 컨설팅',
	title: '김세진 소상공인 컨설턴트 | 현장 진단부터 온라인 매출까지',
	description:
		'소상공인 전문 컨설턴트 김세진. 매장 현장 진단, 온라인 마케팅, 정부지원사업 준비를 1:1로 돕고, LMS VOD 과정으로 언제든 다시 배울 수 있습니다.',
} as const;

export const CONTACT = {
	name: '김세진',
	role: '소상공인 컨설턴트',
	phone: '010-8624-8866',
	phoneHref: 'tel:01086248866',
	email: 'trendwatcher@nate.com',
	emailHref: 'mailto:trendwatcher@nate.com',
	address: '경기 하남시 미사대로 520 C동 607호',
} as const;

/** LMS(온라인 강의) 사이트 주소. 실제 주소를 받으면 이 줄만 바꾸세요. */
export const LMS_URL = '#courses';
