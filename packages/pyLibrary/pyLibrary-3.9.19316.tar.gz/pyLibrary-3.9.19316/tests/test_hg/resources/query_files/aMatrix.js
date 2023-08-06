/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


Matrix=function(arg){
  //THIS IS A DATA CUBE, WITH ONLY INTEGER INDICES
  //THIS IS NOT A STANDARD MATHEMATICAL MATRIX
  //
  // data - If you alreay have an Array (or Array of Arrays) and want to index it as volume
  //
  // OR
  //
  // dim - Array of integers for the shape
  // constructor - parameter-free function to generate cell values
  //

  function makeArray(length, constructor){
    return function(){
      var output = [];
      for(var i=length;i--;){
        output[i]=constructor();
      }//for
      return output;
    };//function
  }//for

  if (arg.data) {
    this.dim = [];
    var d = arg.data;
    while (d instanceof Array) {
      this.dim.append(d.length);
      d = d[0];
    }//while
    this.num = this.dim.length;
    if (this.num == 0 && typeof(arg.data) == "object") {
      Log.error("Expecting an array");
    }//endif
    this.data = arg.data;
  }else if (arg.dim instanceof Array){
    var self=this;
    this.num=arg.dim.length;
    this.dim=arg.dim;
    var c = arg.constructor;
    if (typeof c != "function") {
      var value = c;
      c = function(){return value;};
    }else if (c.isFrozen!==undefined){  //JAVASCRIPT CONSTRUCTOR
      c = function(){};
    }//endif

    //BUILD A STACK OF FUNCTIONS TO MAKE Matrix
    Array.reverse(Array.newRange(0, this.num)).forall(function(i){
      c = makeArray(self.dim[i], c);
    });
    //RUN OUR STACK
    this.data=c();
  }else if (arg instanceof Array){
    //EXPECTING COORDINATES ARRAY
    this.num=arg.length;
    this.dim=arg;
  }else{
    Log.error("not supported")
  }//endif
  return this;
};//function



//PROVIDE func(v, i, c, cube) WHERE
// v - IS A VALUE IN THE CUBE
// i - IS THE INDEX INTO THE edge
// c - AN ARRAY OF COORDINATES v IS FOUND AT
// cube - THE WHOLE CUBE
// NOTE: c[edge]==i
function forall1(edge, func){
  var data = this.data;
  var num = this.num;
  var c = [];

  function iter(v, d){
    if (d == num) {
      func(v, c[edge], c, data);
    } else {
      for (var j = 0; j < v.length; j++) {
        c[d] = j;
        iter(v[j], d + 1);
      }//for
    }//endif
  }//function
  iter(data, 0);
}


//PROVIDE func(v, c, cube) WHERE
// v - IS A VALUE IN THE CUBE
// c - AN ARRAY OF COORDINATES v IS FOUND AT
// cube - THE WHOLE CUBE
Matrix.prototype.forall = function(func, other){
  if (other!==undefined){
    Log.error("No longer supported, use the simpler version");
  }//endif

  var data = this.data;
  var num = this.num;
  var c = [];

  function iter(v, d){
    if (d == num) {
      func(v, c, data);
    } else {
      for (var j = 0; j < v.length; j++) {
        c[d] = j;
        iter(v[j], d + 1);
      }//for
    }//endif
  }//function
  iter(data, 0);
};


Matrix.prototype.map = function (func) {
//PROVIDE func(v, c, cube) WHERE
// v - IS A VALUE IN THE CUBE
// c - AN ARRAY OF COORDINATES v IS FOUND AT
// cube - THE WHOLE CUBE
// func MUST RETURN A NEW VALUE
  var data=this.data;
  var num = this.num;
  var c = [];

  function iter(v, d) {
    if (d == num) {
      return func(v, c, data);
    } else {
      var output=[];
      for (var j = 0; j < v.length; j++){
        c[d]=j;
        output.append(iter(v[j], d+1));
      }//for
      return output;
    }//endif
  }//function
  return iter(data, 0);
};

/*
 * RETURN A NEW MATRIX WITH LESS COORDINATES
 * slice - AN ARRAY OF SLICES
 * EACH SUB-SLICE IS
 *  * undefined - TO INDICATE ALL
 *  * AN ARRAY OF VALUES TO BE KEPT
 *  * RANGE {"min":min, "max":max}, BOTH PARAMETERS OPTIONAL
 */
Matrix.prototype.slice=function(slice){

  function _slicer(_slice, data){
    var slice=_slice[0];

    if (_slice.length==1){
      if (slice===undefined){
        return data;
      }else if (Array.isArray(slice)){
        return data.map(function(m, i){
          if (slice.contains(i)) return m;
        });
      }else{
        return data.map(function(m, i){
          if (slice.min === undefined) {
            if (slice.max === undefined) {
              return m;
            } else {
              if (i < slice.max) return m;
            }//endif
          } else {
            if (slice.max === undefined) {
              if (i >= slice.min) return m;
            } else {
              if (slice.min <= i && i < slice.max) return m;
            }//endif
          }//endif
        });
      }//endif
    }else{
      if (slice===undefined){
        return data.map(function(d){return _slicer(_slice.slice(1), d);});
      }else if (Array.isArray(slice)){
        return data.map(function(d, i){
          if (slice.contains(i)) return _slicer(_slice.slice(1), d);
        });
      }else{
        return data.map(function(d, i){
          if (slice.min === undefined) {
            if (slice.max === undefined) {
              return _slicer(_slice.slice(1), d);
            } else {
              if (i < slice.max) return _slicer(_slice.slice(1), d);
            }//endif
          } else {
            if (slice.max === undefined) {
              if (i >= slice.min) return _slicer(_slice.slice(1), d);
            } else {
              if (slice.min <= i && i < slice.max) return _slicer(_slice.slice(1), d);
            }//endif
          }//endif
        });
      }//endif
    }//endif
  }

  if (slice.length<this.dim.length) slice[this.dim.length-1]=undefined;
  var newData = new Matrix({"data":_slicer(slice, this.data)});
  return newData;
};


//PROVIDE func(v, i, c, cube) WHERE
// v - IS A SUB-CUBE
// i - IS THE INDEX INTO THE edge
// c - AN ARRAY OF PARTIAL COORDINATES v IS FOUND AT
// cube - THE WHOLE CUBE
// func MUST RETURN A SUBCUBE, OR undefined
Matrix.prototype.filter = function (edge, func) {
  var data=this.data;
  var c = [];

  function iter(v, d) {
    var output=[];
    if (d == edge) {
      for (var k = 0; k < v.length; k++) {
        var u = func(v[k], k, c, data);
        if (u!==undefined) output.append(u);
      }//for
    } else {
      for (var j = 0; j < v.length; j++) {
        c[d]=j;
        output.append(iter(v[j], d+1));
      }//for
    }//endif
    return output;
  }//function
  return iter(data, 0);
};

// keep - ORDERED LIST OF DIMENSIONS WE ITERATE OVER
// func MUST RETURN A SUBCUBE, OR undefined AND
// MUST BE func(v, i, c, cube) WHERE
// v - IS A SUB-CUBE
// c - AN ARRAY OF COORDINATES v IS FOUND AT, IN keep ORDER
// cube - THE WHOLE CUBE
//
// func MUST RETURN A CUBE OF EQUAL SIZE
Matrix.prototype.mapN = function(keep, func){
  var self = this;
  var remainder = self.dim.map(function(d, i){if (!keep.contains(i)) return i;});
  var perm = [].extend(keep).extend(remainder);
  var num = keep.length;

  var work = self.transpose(perm);
  var c=[];
  function iter(v, d) {
    if (d == num) {
      return func(v, c, self);
    } else {
      var output=[];
      for (var j = 0; j < v.length; j++) {
        c[d]=j;
        output.append(iter(v[j], d+1));
      }//for
      return output;
    }//endif
  }//function
  var result = new Matrix({"data": iter(work.data, 0)});

  var rev = perm.map(function(c, i){return perm.indexOf(i);});
  return result.transpose(rev);
};


// perm - ARRAY WITH DIMENSION PERMUTATION
Matrix.prototype.transpose = function(perm){
  var self = this;
  if (perm.length!=self.dim.length){
    Log.error("Expecting permulation to have length equal to cube dimensions")
  }//endif
  var output = new Matrix({"dim": perm.map(function(k){return self.dim[k];})});

  self.forall(function(v, coord){
    var newCoord = [];
    for(var i=coord.length;i--;) newCoord[i]=coord[perm[i]];
    output.set(newCoord, self.get(coord));
  });
  return output;
};

Matrix.prototype.get=function(coord){
  if (coord.length!=this.num){
    Log.error("expecting coordinates of "+this.num+" dimensions")
  }//endif
  var d=this.data;
  for(var i=0;i<coord.length;i++){
    d=d[coord[i]];
  }//for
  return d;
};

Matrix.prototype.set=function(coord, value){
  if (coord.length!=this.num){
    Log.error("expecting coordinates of "+this.num+" dimensions")
  }//endif
  var d=this.data;
  for(var i=0;i<coord.length-1;i++){
    d=d[coord[i]];
  }//for
  d[coord[this.num-1]]=value;
  return this;
};
