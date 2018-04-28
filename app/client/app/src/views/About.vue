<template>
  <section>
    <div class="team">
        <h3>Team</h3>
        <div class="member">
            <a class="left" href="https://github.com/rebeccabernie" v-tooltip.top-center="'Rebecca Kane'">
                <img src="../assets/img/rebecca.jpg">
            </a>
            <div class="vertical-space left"></div>
            <a class="right" href="https://github.com/taraokelly" v-tooltip.top-center="'Tara O\'Kelly'">
                <img src="../assets/img/tara.jpg"/>
            </a>
        </div>
    </div>
    <div class="spacer"></div>
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          About
        </p>
      </header>
      <div class="card-content">
        <div class="content">
          Currency Analyser is an applied project assisting the research of the viability and volatility of cryptocurrency. Bitcoin, being the most prevalent cryptocurrency, is the subject of our analysis. 
          <br><br>
          This web application features:
          <ul>
              <li>A comparison of the last ten minutes of traditional currency and Bitcoin data. It is clear from examining this data that Bitcoin typically has a higher level of volatility than that of traditional currencies.  </li>
              <li>A prediction of Bitcoin’s close price for the current day. Also provided is a comparison of past predictions, along with the corresponding actual close prices.</li>
          </ul>
          <br>
         Applied Project and Dissertation, (Honours) Software Development, Galway-Mayo Intstitue of Technology.
        </div>
      </div>
    </div>
    <div class="spacer"></div>
    <a class="repo" href="https://github.com/rebeccabernie/CurrencyAnalyser" v-tooltip.top-center="'Repository'">
        <img src="../assets/img/git.png"/>
    </a>

  </section>
</template>

<script>
/*
The about view contains information and resources concerning this applied project.
 */
export default {
  name: 'About'
}
</script>
<style>

.spacer { clear: both; height: 30px; display: block; }
.spacer-small { clear: both; height: 10px; display: block; }
.team { width: 175px; margin: 0 auto; }
.repo{ margin: 0 auto; display: block; }
.repo, .repo img{ height: 35px; width: 35px; }
.team h3{
    font-weight: 700;
    padding: 0.75rem;
    text-align:center;
    flex-grow: 1;
    font-size: 1.2rem;
    margin: -20px 0 10px auto;
}
.team .member img{
 -webkit-border-radius: 50%;
 -moz-border-radius: 50%;
 border-radius: 50%;
 height: 75px;
 width: 75px;
}
.team .member a{ height: 75px; width: 75px; }
.team-info{ width:75px; display: block; margin: 0 auto; }
.team-info img{
 -webkit-border-radius: 50%;
 -moz-border-radius: 50%;
 border-radius: 50%;
 height: 75px;
 width: 75px;
}
.team-info a{ height: 75px; width: 75px; }
.team .member .vertical-space{ width: calc(100% - 150px); }
.right{ float:right; }
.left{ float: left; }
.tooltip { display: block !important; z-index: 10000; }
.tooltip .tooltip-inner {
  background: rgba(0,0,0,0.6);
  color: white;
  border-radius: 16px;
  padding: 5px 10px 4px;
}
.tooltip .tooltip-arrow {
  width: 0;
  height: 0;
  border-style: solid;
  position: absolute;
  margin: 5px;
  border-color: rgba(0,0,0,0.6);
}
.tooltip[x-placement^="top"] { margin-bottom: 5px; }
.tooltip[x-placement^="top"] .tooltip-arrow {
  border-width: 5px 5px 0 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  bottom: -5px;
  left: calc(50% - 5px);
  margin-top: 1px;
  margin-bottom: 0;
}
.tooltip-arrow{ top: calc(50% + 15px); }
.tooltip[x-placement^="bottom"] { margin-top: 5px; }
.tooltip[x-placement^="bottom"] .tooltip-arrow {
  border-width: 0 5px 5px 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-top-color: transparent !important;
  top: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}
.tooltip[x-placement^="right"] { margin-left: 5px; }
.tooltip[x-placement^="right"] .tooltip-arrow {
  border-width: 5px 5px 5px 0;
  border-left-color: transparent !important;
  border-top-color: transparent !important;
  border-bottom-color: transparent !important;
  left: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}
.tooltip[x-placement^="left"] { margin-right: 5px; }
.tooltip[x-placement^="left"] .tooltip-arrow {
  border-width: 5px 0 5px 5px;
  border-top-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  right: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}
.tooltip[aria-hidden='true'] { visibility: hidden; opacity: 0; transition: opacity .15s, visibility .15s; }
.tooltip[aria-hidden='false'] { visibility: visible; opacity: 1; transition: opacity .15s; }
</style>