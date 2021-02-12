export const reverseArr = (input: Array<any>) => {
    var ret = new Array<any>();
    for(var i = input.length-1; i >= 0; i--) {
        ret.push(input[i]);
    }
    return ret;
}