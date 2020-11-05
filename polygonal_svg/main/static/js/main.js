function animateSvg(svg2, tab) {

    const svg1 = document.querySelectorAll(`#${tab}Svg polygon`)

    const svg1Len = svg1.length
    const svg2Len = svg2.length

    const lenMin = Math.min(svg1Len, svg2Len)
    const lenDiff = Math.abs(svg1Len - svg2Len)

    const aDuration = 2500;
    const aDelay = 500;
    const aAttitude = 1.4

    const aVisibleTime = aDuration / (lenMin + lenDiff*aAttitude);
    const aUnvisibleTime = aDuration / (lenMin + lenDiff);

    if (svg1Len < svg2Len) {
        const svgElem = document.querySelector(`#${tab}Svg`)
        for (let i=0; i < svg2Len - svg1Len; ++i) {
            const defaultPolygon = document.createElementNS(
                'http://www.w3.org/2000/svg', 'polygon'
            )
            defaultPolygon.setAttribute(
                'id', svg2[svg1Len + i].id.slice(1)
            )
            defaultPolygon.setAttribute(
                'points', svg2[svg1Len + i].points
            )
            defaultPolygon.style.opacity = '0'

            svgElem.appendChild(defaultPolygon);
        }
    }

    let timeline = anime.timeline({
        direction: 'alternate',
        loop: true,
        autoplay: true,
        easing: 'easeInOutQuad',
        duration: aDuration
    })

    timeline.add({
        targets: 'polygon:first-child',
        opacity: 1,
        duration: aDelay
    });

    if (svg1Len < svg2Len) {
        svg2.forEach((polygon, index) => {
            if (index < svg1Len) {
                timeline.add({
                    targets: polygon.id,
                    points: polygon.points,
                    translateX: 1200,
                }, aDelay + aVisibleTime * index)
            }
            else {
                timeline.add({
                    targets: polygon.id,
                    opacity: 1,
                    translateX: 1200,
                }, aDelay + aUnvisibleTime * index)
            }
        })
    }
    else {
        svg1.forEach((polygon, index) => {
            if (index < svg2Len) {
                timeline.add({
                    targets: svg2[index].id,
                    points: svg2[index].points,
                    translateX: 1200,
                }, aDelay + aVisibleTime * index)
            }
            else {
                timeline.add({
                    targets: polygon,
                    opacity: 0,
                    translateX: -1200,
                }, aDelay + aUnvisibleTime * index)
            }
        })
    }

    timeline.add({
        targets: 'polygon:first-child',
        opacity: 1,
        duration: aDelay
    });
}

function showCurrentTab() {
    let tab = localStorage.getItem('currentTab')
    if (!tab) {tab = 'examples'}

    const tabLink = document.querySelector(`.nav-link.${tab}`)
    tabLink.classList.add('active')

    const tabContent = document.querySelector(`.tab-pane#${tab}`)
    tabContent.classList.add('show')
    tabContent.classList.add('active')
}

$(function () {
    // Список всех вкладок
    const allTabs = ['examples', 'user']

    // Открытие текущей вкладки и анимирование SVG
    showCurrentTab()
    getExampleSvgData().then(svg2 => animateSvg(svg2, 'examples'))
    getUserSvgData().then(svg2 => animateSvg(svg2, 'user'))

    // Сохранение текущей вкладки в localStorage и сброс данных форм
    document.querySelectorAll('.nav-link').forEach((tabLink) => {
        tabLink.addEventListener('click', (e) => {
            localStorage.setItem(
                'currentTab', e.target.getAttribute('href').slice(1)
            )
            allTabs.forEach((tab) => {
                document.querySelector(`.tab-pane#${tab} form`).reset()
            })
        })
    })
})