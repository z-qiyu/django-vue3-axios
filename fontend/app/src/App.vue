<template>
  <router-view/>
</template>

<style lang="scss">

::-webkit-srollbar-track-piece{background:none;-webkit-border-radius:0;}
::-webkit-scrollbar{width:8px;height:8px;}
::-webkit-scrollbar-thumb:vertical{height:50px;background-color:#bbbbbb;-webkit-border-radius:4px;outline:0px solid #ffffff;ouline-offset:-2px;border:2px solid #ffffff;}
::-webkit-scrollbar-thumb:hover{height:50px;background-color:#999999;-webkit-border-radius:4px;}
::-webkit-scrollbar-thumb:horizontal{width:50px;background-color:#bbbbbb;-webkit-border-radius:4px;outline:0px solid #ffffff;ouline-offset:-2px;border:2px solid #ffffff;}


#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
