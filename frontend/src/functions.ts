
function execAfterPywebviewLoaded(func: () => void) {
  const interval_id = setInterval(() => {
    if (window.pywebview) {
      try {
        func();
        clearInterval(interval_id);
      }
      catch (e) {
        console.error("[handled exception at execAfterPywebviewLoaded]" + e)
      }
    }
  }, 100);
}

function getSubjectType(subject_type_id: number): string {
  if (subject_type_id === 1) {
    return "书籍"
  } else if (subject_type_id === 2) {
    return "动画"
  } else if (subject_type_id === 3) {
    return "音乐"
  } else if (subject_type_id === 4) {
    return "游戏"
  } else if (subject_type_id === 6) {
    return "三次元"
  }
  return "未知"
}

function getEditCollectVerbList(subject_type_id: number): string[] {
  if (subject_type_id === 1) {
    return [
      "想看",
      "看过",
      "在看",
      "搁置",
      "抛弃"
    ]
  } else if (subject_type_id === 2) {
    return [
      "想看",
      "看过",
      "在看",
      "搁置",
      "抛弃"
    ]
  } else if (subject_type_id === 3) {
    return [
      "想听",
      "听过",
      "在听",
      "搁置",
      "抛弃"
    ]
  } else if (subject_type_id === 4) {
    return [
      "想玩",
      "玩过",
      "在玩",
      "搁置",
      "抛弃"
    ]
  } else if (subject_type_id === 6) {
    return [
      "想看",
      "看过",
      "在看",
      "搁置",
      "抛弃"
    ]
  } else {
    return [
      "想看",
      "看过",
      "在看",
      "搁置",
      "抛弃"
    ]
  }
}


const theme_list = ['cupcake', 'night', 'nord', 'emerald', 'retro', 'cyberpunk', 'valentine', 'halloween', 'garden', 'forest']

async function getCurrentTheme() {
  const currentTheme = await window.pywebview.api.getCurrentTheme()
  if (theme_list.includes(currentTheme)) {
    return currentTheme
  } else {
    return 'cupcake'
  }
}

async function applyCurrentTheme() {
  const currentTheme = await getCurrentTheme()
  document.documentElement.setAttribute('data-theme', currentTheme);
}

async function setCurrentTheme(theme: string) {
  if (theme_list.includes(theme)) {
    await window.pywebview.api.setCurrentTheme(theme)
  }
  await applyCurrentTheme()
}

export {
  getSubjectType,
  execAfterPywebviewLoaded,
  getEditCollectVerbList,
  getCurrentTheme,
  setCurrentTheme,
  applyCurrentTheme,
  theme_list
}
