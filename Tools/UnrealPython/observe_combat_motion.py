"""Read-only motion sampling for live_gameplay_operator.py in an active mission.

Install after that operator, then unregister its control callback if using the
full playthrough driver. This observer never changes transforms or combat data.
"""
motion_trace={'rows':[],'last':-1,'last_write':-1,'handle':None}
def motion_observe(dt,s=motion_trace):
 if not unreal.SystemLibrary.is_valid(live_player):unreal.unregister_slate_post_tick_callback(s['handle']);return
 t=live_gs.get_time_seconds(live_world)
 if t-s['last']<.08:return
 snap=live_snapshot();s['rows'].append(snap);s['last']=t
 if t-s['last_write']>2:
  with open(os.path.join(live_folder,'refined-motion.json'),'w') as f:json.dump({'real_gameplay_observation':True,'no_stat_overrides':True,'samples':s['rows']},f)
  s['last_write']=t
motion_trace['handle']=unreal.register_slate_post_tick_callback(motion_observe)
unreal.log('LIVE_STATE '+json.dumps(live_snapshot()))
