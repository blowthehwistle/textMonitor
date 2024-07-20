(function() {
    // 기존의 pushState와 replaceState를 저장합니다.
    const originalPushState = history.pushState;
    const originalReplaceState = history.replaceState;

    // 플래그 설정
    let ignorePopstate = false;

    // pushState와 replaceState를 확장하여 popstate 이벤트를 수동으로 트리거합니다.
    history.pushState = function() {
        const result = originalPushState.apply(history, arguments);
        if (!ignorePopstate) {
            console.log("pushState로 인한 popstate 트리거");
            window.dispatchEvent(new Event('manualpopstate'));
        }
        return result;
    };

    history.replaceState = function() {
        const result = originalReplaceState.apply(history, arguments);
        if (!ignorePopstate) {
            console.log("replaceState로 인한 popstate 트리거");
            window.dispatchEvent(new Event('manualpopstate'));
        }
        return result;
    };

    window.addEventListener('load', function() {
        console.log("페이지 로드 완료. 뒤로가기 방지 기능 초기화.");
        // 페이지가 로드될 때 현재 상태를 추가하여 뒤로 가기 방지 기능을 초기화합니다.
        ignorePopstate = true;
        history.replaceState(null, null, location.href);
        ignorePopstate = false;
    });

    window.addEventListener('popstate', function(event) {
        if (ignorePopstate) {
            console.log("ignorePopstate가 설정된 popstate 이벤트 무시.");
            return;
        }
        console.log("popstate 이벤트 발생. 뒤로가기 방지.");
        ignorePopstate = true;
        history.replaceState(null, null, location.href);
        ignorePopstate = false;

        // 경고 메시지를 표시합니다.
        alert('뒤로가기 방지! 목록으로 돌아가기 버튼을 눌러주세요.');
    });

    window.addEventListener('manualpopstate', function(event) {
        console.log("manualpopstate 이벤트 발생.");
        // 이 이벤트는 manualpopstate에서만 처리하며, 뒤로가기 방지 처리에 영향을 주지 않습니다.
    });
})();