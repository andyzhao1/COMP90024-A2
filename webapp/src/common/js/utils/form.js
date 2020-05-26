export function emptyToNull (form) {
  let newForm = {}
  for (let key in form) {
    if (form[key] === '') {
      newForm[key] = null
    } else {
      newForm[key] = form[key]
    }
  }
  return newForm
}
